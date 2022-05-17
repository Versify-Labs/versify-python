from audioop import add
import os
import time
from typing import Tuple
from urllib.parse import urlparse

import boto3
import requests
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.logging.logger import Logger
from aws_lambda_powertools.tracing import Tracer
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
from pynamodb.exceptions import DoesNotExist
from versify.utilities.model import generate_uuid

from .model import AirdropModel, FulfillmentModel, OrderModel

ENVIRONMENT = os.environ['ENVIRONMENT']
if ENVIRONMENT == 'prod':
    VERSIFY_API_URL = 'https://api.versifylabs.com'
else:
    VERSIFY_API_URL = 'https://api-dev.versifylabs.com'

logger = Logger()
tracer = Tracer()
metrics = Metrics(namespace="versify")


@tracer.capture_method
def call_internal_api(path: str, body: dict = {}, organization: str = None) -> Tuple[bool, str]:
    url = urlparse(VERSIFY_API_URL)
    region = boto3.session.Session().region_name
    iam_auth = BotoAWSRequestsAuth(
        aws_host=url.netloc,
        aws_region=region,
        aws_service='execute-api'
    )
    headers = {'Organization': organization}
    logger.info({
        'url': VERSIFY_API_URL+path,
        'json': body,
        'auth': iam_auth,
        'headers': headers
    })
    response = requests.get(
        VERSIFY_API_URL+path,
        json=body,
        auth=iam_auth,
        headers=headers
    )
    logger.debug({
        "message": "Response received from internal api",
        "body": response.json()
    })
    return response.json()


def get_customer(organization, id):
    path = '/backend/customers/' + id
    return call_internal_api(path, {}, organization)


def get_merchant(organization, id):
    path = '/backend/organizations/' + id
    return call_internal_api(path, {}, organization)


def get_product(organization, id):
    path = '/backend/products/' + id
    return call_internal_api(path, {}, organization)


def list_wallet_addresses(email):
    path = f'/backend/wallets/{email}/blockchain_addresses'
    return call_internal_api(path, {})


class Airdrops:

    def __init__(self, email: str = None, organization: str = None):
        self.model = AirdropModel
        self.email = email
        self.organization = organization

    def to_list(self, items):
        return [item.to_dict() for item in items]

    def inject_fields(self, body: dict):
        """Inject fields into the airdrop and return the airdrop"""
        logger.info({'airdrop': body})

        # Remove stale data from previous object
        body.pop('version', None)

        # Inject general data
        id = generate_uuid('airdrop')
        body['PK'] = id
        body['SK'] = id
        body['id'] = id
        body["date_created"] = int(time.time())
        body["date_updated"] = int(time.time())
        body['object'] = 'airdrop'
        body['organization'] = self.organization

        logger.info({'airdrop': body})
        return body

    def create(self, body: dict = {}, raw: bool = True):
        """Create a new airdrop"""
        body = self.inject_fields(body)
        airdrop = self.model(**body)
        airdrop.save()
        return airdrop.to_dict() if raw else airdrop


class Fulfillments:

    def __init__(self, email: str = None, organization: str = None):
        self.model = FulfillmentModel
        self.email = email
        self.organization = organization

    def to_list(self, items):
        return [item.to_dict() for item in items]

    def get_order(self, id):
        orders = Orders(self.email, self.organization)
        return orders.get(id)

    def inject_fields(self, body: dict):
        """Inject fields into the fulfillment and return the fulfillment"""
        logger.info({'fulfillment': body})

        # Remove stale data from previous object
        body.pop('version', None)

        # Inject general data
        id = generate_uuid('fulfillment')
        body['PK'] = body['order']
        body['SK'] = id
        body['id'] = id
        body["date_created"] = int(time.time())
        body["date_updated"] = int(time.time())
        body['email'] = self.email
        body['object'] = 'fulfillment'

        # Inject wallet data
        # TODO: Only fetch same blockchain as the order products
        addresses = list_wallet_addresses(self.email)
        logger.info(addresses)
        body['blockchain_address'] = addresses['data'][0]['address']

        # Inject order data
        order = self.get_order(body['order'])
        body['items'] = order['items']
        body['organization'] = order['merchant']

        logger.info({'fulfillment': body})
        return body

    def create(self, order_id: str, body: dict = {}, raw: bool = True):
        """Create a new fulfillment"""
        body['order'] = order_id
        body = self.inject_fields(body)
        fulfillment = self.model(**body)
        fulfillment.save()
        return fulfillment.to_dict() if raw else fulfillment

    def list_by_order(self, order_id: str, query: dict = {}, raw: bool = True):
        """List fulfillments by order"""
        fulfillments = self.model.by_order_by_object.query(
            hash_key=order_id,
            range_key_condition=self.model.object == 'fulfillment'
        )
        return self.to_list(fulfillments) if raw else fulfillments

    def get(self, order_id: str, id: str, raw: bool = True):
        """Retrieves a fulfillment by its id"""
        try:
            item = self.model.get(order_id, id)
        except DoesNotExist:
            return None
        return item.to_dict() if raw else item

    def update(self, order_id: str, id: str, body: dict = {}, raw: bool = True):
        """Update an existing fulfillment"""
        fulfillment = self.get(order_id, id, raw=False)
        actions = []
        for k, v in body.items():
            attr = getattr(self.model, k)
            actions.append(attr.set(v))
        fulfillment.update(actions=actions)
        return fulfillment.to_dict() if raw else fulfillment

    def update_with_txn(self, transaction):
        order_id = transaction['metadata']['order']
        fulfillment_id = transaction['metadata']['fulfillment']
        body = {
            'status': 'fulfilled' if transaction['success'] else 'unfulfilled'
        }
        return self.update(order_id, fulfillment_id, body)


class Orders:

    def __init__(self, email: str = None, organization: str = None):
        self.model = OrderModel
        self.email = email
        self.organization = organization

    def to_list(self, items):
        return [item.to_dict() for item in items]

    def get_filter_condition(self, query):
        params = ['customer', 'fulfillment_status']
        condition = None
        for k, v in query.items():
            if k in params:
                condition &= getattr(self.model, k) == v
        return condition

    def inject_fields(self, body: dict):
        """Inject fields into the order and return the order"""
        logger.info({'order': body})

        # Remove stale data from previous object
        body.pop('version', None)

        # Inject general data
        id = generate_uuid('order')
        body['PK'] = id
        body['SK'] = id
        body['id'] = id
        body["date_created"] = int(time.time())
        body["date_updated"] = int(time.time())
        body['object'] = 'order'
        body['organization'] = self.organization

        # Inject customer data
        body['customer_details'] = get_customer(
            self.organization, body['customer'])
        body['email'] = body['customer_details']['email']

        # Inject merchant data
        body['merchant'] = body['organization']
        body['merchant_details'] = get_merchant(
            self.organization, body['organization'])

        # Inject item products data
        for item in body['items']:
            item['product_details'] = get_product(
                self.organization, item['product'])

        # Inject price data
        amount_total = 0
        for item in body['items']:
            item_total = item.get('price', 0) * item.get('quantity', 1)
            amount_total += item_total
        body['amount_subtotal'] = amount_total
        body['amount_total'] = amount_total

        logger.info({'order': body})
        return body

    def create(self, body: dict = {}, raw: bool = True):
        """Create a new order"""
        body = self.inject_fields(body)
        order = self.model(**body)
        order.save()
        return order.to_dict() if raw else order

    def list_by_email(self, query: dict = {}, raw: bool = True):
        """List orders by wallet email"""
        filter_condition = self.get_filter_condition(query)
        orders = self.model.by_email_by_object.query(
            hash_key=self.email,
            range_key_condition=self.model.object == 'order',
            filter_condition=filter_condition,
        )
        return self.to_list(orders) if raw else orders

    def list_by_organization(self, query: dict = {}, raw: bool = True):
        """List orders by organization"""
        filter_condition = self.get_filter_condition(query)
        orders = self.model.by_organization_by_object.query(
            hash_key=self.organization,
            range_key_condition=self.model.object == 'order',
            filter_condition=filter_condition,
        )
        return self.to_list(orders) if raw else orders

    def get(self, id: str, raw: bool = True):
        """Retrieves an order by its id"""
        try:
            item = self.model.get(id, id)
        except DoesNotExist:
            return None
        return item.to_dict() if raw else item

    def update(self, id: str, body: dict = {}, raw: bool = True):
        """Update an existing order"""
        order = self.get(id, raw=False)
        actions = []
        for k, v in body.items():
            attr = getattr(self.model, k)
            actions.append(attr.set(v))
        order.update(actions=actions)
        return order.to_dict() if raw else order

    def create_order_from_airdrop(self, airdrop):
        body = dict(airdrop)
        body['airdrop'] = airdrop['id']
        body['payment_status'] = 'complete'
        body['type'] = 'airdrop'
        return self.create(body)

    def create_order_from_cart(self, cart):
        body = dict(cart)
        body['cart'] = cart['id']
        body['type'] = 'cart'
        return self.create(body)

    def update_order_with_fulfillment(self, fulfillment):
        order_id = fulfillment['order']
        body = {'fulfillment_status': fulfillment['status']}
        return self.update(order_id, body)


class Versify:

    def __init__(self, email: str = None, organization: str = None):
        self.airdrops = Airdrops(email, organization)
        self.fulfillments = Fulfillments(email, organization)
        self.orders = Orders(email, organization)
