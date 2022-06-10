import os
import time
from typing import Tuple
from urllib.parse import urlparse

import boto3
import requests
from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from aws_lambda_powertools.logging.logger import Logger
from aws_lambda_powertools.tracing import Tracer
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth
from pynamodb.exceptions import DoesNotExist
from versify.utilities.model import generate_uuid

from .model import Airdrop as AirdropModel
from .model import Campaign as CampaignModel

ENVIRONMENT = os.environ['ENVIRONMENT']
VERSIFY_API_VERSION = 'v1'
if ENVIRONMENT == 'prod':
    VERSIFY_API_URL = 'https://api.versifylabs.com'
    VERSIFY_URL = 'https://dashboard.versifylabs.com'
else:
    VERSIFY_API_URL = 'https://api-dev.versifylabs.com'
    VERSIFY_URL = 'https://dashboard-dev.versifylabs.com'

logger = Logger()
tracer = Tracer()
metrics = Metrics()


@tracer.capture_method
def call_internal_api(path: str, body: dict = {}, organization: str = None, params: dict = {}) -> Tuple[bool, str]:
    url = urlparse(VERSIFY_API_URL)
    region = boto3.session.Session().region_name
    iam_auth = BotoAWSRequestsAuth(
        aws_host=url.netloc,
        aws_region=region,
        aws_service='execute-api'
    )
    headers = {'X-Organization': organization}
    logger.info({
        'url': VERSIFY_API_URL+path,
        'params': params,
        'json': body,
        'auth': iam_auth,
        'headers': headers
    })
    response = requests.get(
        VERSIFY_API_URL+path,
        params=params,
        json=body,
        auth=iam_auth,
        headers=headers
    )
    logger.debug({
        "message": "Response received from internal api",
        "body": response.json()
    })
    result = response.json()
    logger.info({
        'result': result
    })
    return result


def get_contact(org_id, contact_id):
    path = f'/crm/{VERSIFY_API_VERSION}/backend/contacts/' + contact_id
    return call_internal_api(path, {}, org_id)


def list_contacts(org_id, filters):
    results = []
    params = {'starting_after': 0,  "filters": filters, }
    has_more = True
    while has_more:
        path = f'/crm/{VERSIFY_API_VERSION}/backend/contacts'
        response = call_internal_api(path, {}, org_id, params)
        results.extend(response['data'])
        if response.get('has_more', False):
            params['starting_after'] = response['data'][-1]['date_created']
        else:
            break
    return results


def get_merchant(org_id):
    path = f'/auth/{VERSIFY_API_VERSION}/backend/organizations/' + org_id
    return call_internal_api(path, {}, org_id)


def get_product(org_id, product_id):
    path = f'/pim/{VERSIFY_API_VERSION}/backend/products/' + product_id
    return call_internal_api(path, {}, org_id)


class Airdrops:

    def __init__(self, organization: str):
        self.model = AirdropModel
        self.organization = organization

    def to_list(self, airdrops):
        return [airdrop.to_dict() for airdrop in airdrops]

    def inject_fields(self, body: dict):
        """Inject fields into the airdrop and return the airdrop"""
        logger.info({'airdrop': body})
        airdrop_id = generate_uuid('airdrop')
        campaign_id = body['campaign']
        org_id = self.organization
        timestamp = int(time.time())
        contact_email = body['contact_details']['email']

        # Remove stale data in case of previous object
        body.pop('version', None)

        # Inject key: getAirdropById(id)
        body['PK'] = airdrop_id

        # Inject key: listAirdropsByOrg(org)
        body['GSI1PK'] = f'{org_id}:airdrop'
        body['GSI1SK'] = timestamp

        # Inject key: listAirdropsByCampaign(campaign)
        body['GSI2PK'] = f'{campaign_id}:airdrop'
        body['GSI2SK'] = timestamp

        # Inject attributes
        body['id'] = airdrop_id
        body['campaign'] = campaign_id
        body['date_created'] = timestamp
        body['date_updated'] = timestamp
        body['object'] = 'airdrop'
        body['organization'] = org_id
        body['mint_details'] = {
            'link': f"{VERSIFY_URL}/claims/{airdrop_id}?email={contact_email}"}

        logger.info({'airdrop': body})
        return body

    def create(self, body: dict = {}, raw: bool = True):
        """Create a new airdrop"""
        body = self.inject_fields(body)
        airdrop = self.model(**body)
        airdrop.save()
        return airdrop.to_dict() if raw else airdrop

    def list_by_org(self, query_params: dict = {}, raw: bool = True):
        """Retrieves a list of airdrops for the org"""
        logger.info(query_params)
        limit = query_params.get('limit', 20)
        before = int(query_params.get('starting_before', 100000000000000)) - 1
        after = int(query_params.get('starting_after', 0)) + 1
        airdrops = self.model.by_organization.query(
            hash_key=f'{self.organization}:airdrop',
            range_key_condition=self.model.GSI1SK.between(after, before),
            limit=limit,
            scan_index_forward=False
        )
        return self.to_list(airdrops) if raw else airdrops

    def list_by_campaign(self, campaign_id, query_params: dict = {}, raw: bool = True):
        """Retrieves a list of airdrops for the org"""
        logger.info(query_params)
        limit = query_params.get('limit', 20)
        before = int(query_params.get('starting_before', 100000000000000)) - 1
        after = int(query_params.get('starting_after', 0)) + 1
        airdrops = self.model.by_campaign.query(
            hash_key=f'{campaign_id}:airdrop',
            range_key_condition=self.model.GSI2SK.between(after, before),
            limit=limit,
            scan_index_forward=False
        )
        return self.to_list(airdrops) if raw else airdrops

    def get(self, airdrop_id, raw: bool = True):
        """Retrieves an airdrop by its id"""
        try:
            airdrop = self.model.get(airdrop_id)
        except DoesNotExist:
            return None
        return airdrop.to_dict() if raw else airdrop

    def update(self, airdrop_id: str, body: dict = {}, raw: bool = True):
        """Update an existing airdrop"""
        airdrop = self.get(airdrop_id, raw=False)
        actions = [self.model.date_updated.set(int(time.time()))]
        for k, v in body.items():
            attr = getattr(self.model, k)
            actions.append(attr.set(v))
        airdrop.update(actions=actions)
        return airdrop.to_dict() if raw else airdrop

    def fulfill(self, airdrop_id: str, body: dict):
        """Fulfill an airdrop"""
        airdrop = self.get(airdrop_id, raw=False)
        if airdrop.status != 'open':
            raise BadRequestError('Airdrop has already been fulfilled')
        mint_details = airdrop.mint_details or {}
        mint_details['address'] = body['address']
        mint_details['email'] = body['email']
        body = {'mint_details': mint_details, 'status': 'pending'}
        airdrop = self.update(airdrop_id, body)
        return airdrop

    def close(self, airdrop_id: str, txn: dict):
        """Close an airdrop so that it cant be fulfilled again"""
        airdrop = self.get(airdrop_id, raw=False)
        if airdrop.status != 'pending':
            raise BadRequestError('Airdrop is not in the pending state')
        # TODO: Update mint_details.address
        # mint_details = airdrop.mint_details
        body = {'status': 'closed'}
        airdrop = self.update(airdrop_id, body)
        return airdrop

    def create_from_campaign(self, campaign_id):
        org_id = self.organization
        campaigns = Campaigns(org_id)
        campaign = campaigns.get(campaign_id, raw=False)

        # TODO: Get all contacts
        filters = campaign.recipients['segment_options']['conditions']
        contacts = list_contacts(self.organization, filters)
        logger.info({'contacts': contacts})

        # TODO: Validate product availability
        # TODO: Validate org billing usage

        # For each recipient, create an airdrop
        for contact in contacts:
            body = {
                'campaign': campaign.id,
                'campaign_details': campaign.to_dict(),
                'contact': contact['id'],
                'contact_details': contact,
                'product': campaign.product,
                'product_details': campaign.product_details,
            }
            self.create(body)

        campaigns.update(campaign.id, {'status': 'complete'})
        return True


class Campaigns:

    def __init__(self, organization: str):
        self.model = CampaignModel
        self.organization = organization

    def get_filter_condition(self, options):

        # Handle View
        view_condition = None
        view = options.get('view', 'all')
        if view == 'draft':
            view_condition = self.model.status == 'draft'
        elif view == 'complete':
            view_condition = self.model.status == 'complete'
        else:
            view_condition = self.model.status == 'draft'
            view_condition |= self.model.status == 'sending'
            view_condition |= self.model.status == 'complete'
        condition = view_condition

        # Handle Query
        query_condition = None
        query_attrs = ['name', 'product']
        query = options.get('query', '')
        for attr in query_attrs:
            if query_condition != None:
                query_condition |= getattr(self.model, attr).contains(query)
            else:
                query_condition = getattr(self.model, attr).contains(query)
        if query_condition != None:
            condition &= query_condition

        # Handle Filter
        filters_condition = None
        filters = options.get('filters', '').split(',')
        filters = [f for f in filters if f.count('-') == 2]
        for f in filters:
            prop, op, val = f.split('-')
            f_condition = None
            if op == 'equal':
                f_condition = getattr(self.model, prop) == val
            elif op == 'notEqual':
                f_condition = getattr(self.model, prop) != val
            elif op == 'contains':
                f_condition = getattr(self.model, prop).contains(val)
            elif op == 'notContains':
                f_condition = ~getattr(self.model, prop).contains(val)
            elif op == 'startsWith':
                f_condition = getattr(self.model, prop).startswith(val)
            elif op == 'greaterThan':
                f_condition = getattr(self.model, prop) > val
            elif op == 'lessThan':
                f_condition = getattr(self.model, prop) < val
            elif op == 'isBlank':
                f_condition = getattr(self.model, prop).does_not_exist()
            elif op == 'isPresent':
                f_condition = getattr(self.model, prop).exists()
            if f_condition != None:
                if filters_condition != None:
                    filters_condition |= f_condition
                else:
                    filters_condition = f_condition
        if filters_condition != None:
            condition &= filters_condition

        logger.info(condition)
        return condition

    def to_list(self, items):
        return [item.to_dict() for item in items]

    def generate_recipients(self, filters: str = ''):
        recipients = {
            'contacts': [],
            'count': 0,
            'segment_options': {
                'match': 'all',
                'conditions': filters
            }
        }
        contacts = list_contacts(self.organization, filters)
        recipients['count'] = len(contacts)
        return recipients

    def inject_fields(self, body: dict):
        """Inject fields into the campaign and return the campaign"""
        logger.info({'campaign': body})
        campaign_id = generate_uuid('campaign')
        org_id = self.organization
        timestamp = int(time.time())

        # Remove stale data in case of previous object
        body.pop('version', None)

        # Inject key: getCampaignById(campaign_id)
        body['PK'] = campaign_id

        # Inject key: listCampaignsByOrg(org_id)
        body['GSI1PK'] = f'{org_id}:campaign'
        body['GSI1SK'] = timestamp

        # Inject key: listCampaignsByOrg(org_id)
        # TODO: Replace with optimization for another query
        body['GSI2PK'] = f'{org_id}:campaign'
        body['GSI2SK'] = timestamp

        # Inject attributes
        body['id'] = campaign_id
        body['date_created'] = timestamp
        body['date_updated'] = timestamp
        body['object'] = 'campaign'
        body['organization'] = org_id

        # Inject product data
        body['product_details'] = get_product(org_id, body['product'])

        # Inject recipient data
        filters = body['recipients']['segment_options']['conditions']
        body['recipients'] = self.generate_recipients(filters)

        logger.info({'campaign': body})
        return body

    def create(self, body: dict = {}, raw: bool = True):
        """Create a new campaign"""
        body = self.inject_fields(body)
        campaign = self.model(**body)
        campaign.save()
        return campaign.to_dict() if raw else campaign

    def list_by_org(self, query_params: dict = {}, raw: bool = True):
        """Retrieves a list of campaigns for the org"""
        logger.info(query_params)
        filter_condition = self.get_filter_condition(query_params)
        limit = query_params.get('limit', 20)
        before = int(query_params.get('starting_before', 100000000000000)) - 1
        after = int(query_params.get('starting_after', 0)) + 1
        campaigns = self.model.by_organization.query(
            hash_key=f'{self.organization}:campaign',
            range_key_condition=self.model.GSI1SK.between(after, before),
            filter_condition=filter_condition,
            limit=limit,
            scan_index_forward=False
        )
        return self.to_list(campaigns) if raw else campaigns

    def get(self, campaign_id: str, raw: bool = True):
        """Retrieves a campaign by its id"""
        try:
            item = self.model.get(campaign_id)
        except DoesNotExist:
            return None
        return item.to_dict() if raw else item

    def update(self, campaign_id: str, body: dict = {}, raw: bool = True):
        """Update an existing campaign"""
        campaign = self.get(campaign_id, raw=False)
        actions = [self.model.date_updated.set(int(time.time()))]
        for k, v in body.items():
            if k == 'recipients':
                filters = v['segment_options']['conditions']
                new_recipients = self.generate_recipients(filters)
                actions.append(self.model.recipients.set(new_recipients))
            else:
                attr = getattr(self.model, k)
                actions.append(attr.set(v))
        campaign.update(actions=actions)
        return campaign.to_dict() if raw else campaign

    def send(self, campaign_id: str):
        """Send an campaign"""
        campaign = self.get(campaign_id, raw=False)
        if campaign.status != 'draft':
            raise BadRequestError('Claim is not in the draft state')
        # TODO: Validate product availability
        # TODO: Validate org billing usage
        body = {'status': 'sending'}
        campaign = self.update(campaign_id, body)
        return campaign

    def add_mint(self, campaign_id: str, qty: int = 1):
        """Close an campaign so that it cant be fulfilled again"""
        campaign = self.get(campaign_id, raw=False)
        campaign_dict = campaign.to_dict()
        results = campaign_dict['results'] or {}
        results['amount_minted'] = results.get('amount_minted', 0) + qty
        body = {'results': results}
        campaign = self.update(campaign_id, body)
        return campaign


class Versify:

    def __init__(self, organization: str = None) -> None:
        self.airdrops = Airdrops(organization)
        self.campaigns = Campaigns(organization)
