import logging
import os
import secrets
import time

from bson.objectid import ObjectId
from pydantic.utils import deep_update
from pymongo.collection import ReturnDocument

from ..config import (AccountConfig, AirdropConfig, ClaimConfig,
                      CollectionConfig, ContactConfig, JourneyConfig,
                      JourneyRunConfig, MessageConfig, MintConfig,
                      MintLinkConfig, ProductConfig, StripeConfig)
from ..utils.exceptions import NotFoundError
from ..utils.expandable import ExpandableResource
from ..utils.images import get_image
from ..utils.mongo import mdb
from ..utils.paragon import Paragon
from ..utils.stripe import stripe

if os.environ.get('ENVIRONMENT', 'dev') == 'prod':
    BILLING_URL = 'https://dashboard.versifylabs.com/admin/settings/business/billing'
else:
    BILLING_URL = 'https://dashboard-dev.versifylabs.com/admin/settings/business/billing'


class AccountService(ExpandableResource):

    def __init__(self) -> None:
        self.collection = mdb[AccountConfig.db][AccountConfig.collection]
        self.expandables = AccountConfig.expandables
        self.Model = AccountConfig.model
        self.object = AccountConfig.object
        self.prefix = AccountConfig.prefix
        self.search_index = AccountConfig.search_index

    def create(self, body: dict) -> dict:
        """Create a new account. If the account already exists, update the account.

        Args:
            account (dict): The account to create.

        Returns:
            dict: The account.
        """
        logging.info('Creating account')

        # Create fields
        account_id = f'{self.prefix}_{ObjectId()}'
        body['_id'] = account_id
        body['account'] = account_id
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Clean up fields
        body['email'] = body['email'].lower()
        body['name'] = body['name'].strip()

        # Create stripe customer to bill account
        stripe_customer = stripe.Customer.create(
            description='Versify Customer',
            email=body['email'],
            metadata={'account': account_id},
            name=body['name']
        )

        # Populate necessary fields
        body['authentication'] = {
            'api_public_key': f'pk_{secrets.token_urlsafe(16)}',
            'api_secret_key': f'sk_{secrets.token_urlsafe(16)}'
        }
        body['billing'] = {
            'stripe_customer_id': stripe_customer['id']
        }
        body['branding'] = {
            'icon': get_image(body['name']),
            'logo': get_image(body['name']),
            'wallet_welcome_message': 'Welcome to ' + body['name'],
            'website_title': f"{body['name']} Rewards Program",
            'website_hero_title':  f"{body['name']} Rewards Program",
        }
        body['team'] = [
            {
                'email': body['email'],
                'role': 'admin'
            }
        ]

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        data = data.to_json()

        return data

    def count(self, filter: dict) -> int:
        """Count accounts.

        Args:
            filter (dict): The filter to use.

        Returns:
            int: The number of accounts.
        """
        logging.info('Counting accounts')

        # Get accounts from DB
        count = self.collection.count_documents(filter)

        return count

    def list(self, filter: dict = {}, limit: int = 20, skip: int = 0) -> list:
        """List accounts.

        Args:
            query (dict): The query to use.

        Returns:
            list: The accounts.
        """
        logging.info('Listing accounts')

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        return data

    def list_by_member_email(self, email: str) -> list:
        """List all accounts that a member is a member of.

        Args:
            email (str): The email of the member to list accounts of.

        Returns:
            list: The accounts.
        """
        logging.info('Listing accounts by member email')

        # Find accounts with member matching email
        accounts = self.collection.find(filter={'team.email': email})

        # Convert to JSON
        accounts = [self.Model(**account).to_json() for account in accounts]

        return accounts

    def retrieve_by_api_secret_key(self, api_key: str) -> dict:
        """Get an account by api key.

        Args:
            api_key (str): The api key of the account to retrieve.

        Returns:
            dict: The account.
        """
        logging.info('Retrieving account')

        # Find document matching filter
        account = self.collection.find_one(
            filter={'authentication.api_secret_key': api_key}
        )
        if not account:
            raise NotFoundError

        # Convert to JSON
        account = self.Model(**account).to_json()

        return account

    def retrieve_by_api_public_key(self, api_key: str) -> dict:
        """Get an account by api key.

        Args:
            api_key (str): The api key of the account to retrieve.

        Returns:
            dict: The account.
        """
        logging.info('Retrieving account')

        # Find document matching filter
        account = self.collection.find_one(
            filter={'authentication.api_public_key': api_key}
        )
        if not account:
            raise NotFoundError

        # Convert to JSON
        account = self.Model(**account).to_json()

        return account

    def retrieve_by_id(self, account_id: str) -> dict:
        """Get an account by id.

        Args:
            account_id (str): The id of the account to retrieve.

        Returns:
            dict: The account.
        """
        logging.info('Retrieving account')

        # Find document matching filter
        account = self.collection.find_one(filter={'_id': account_id})
        if not account:
            raise NotFoundError

        # Convert to JSON
        account = self.Model(**account).to_json()

        return account

    def update(self, account_id: str, body: dict) -> dict:
        """Update a account. If the account does not exist, create a new account.

        Args:
            account_id (str): The id of the account to update.
            body (dict): The fields to update.

        Returns:
            dict: The account.

        Raises:
            NotFoundError: If the account does not exist.
        """
        logging.info('Updating account')

        # Find document matching filter
        account = self.collection.find_one(filter={'_id': account_id})
        if not account:
            raise NotFoundError

        # Update fields
        account = deep_update(account, body)
        account['updated'] = int(time.time())

        # Validate against schema
        validated_account = self.Model(**account)

        # Update item in DB
        data = self.collection.find_one_and_update(
            filter={'_id': account_id},
            update={'$set': validated_account.to_bson()},
            upsert=True,
            return_document=ReturnDocument.AFTER
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def delete(self, account_id: str) -> bool:
        """Delete an account.

        Args:
            account_id (str): The id of the account to delete.

        Returns:
            bool: True if the account was deleted, False otherwise.
        """
        logging.info('Deleting account')

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete({
            '_id': account_id,
            'account': account_id,
        })
        if not deleted:
            raise NotFoundError

        return True

    def create_member(self, account_id, body: dict) -> dict:
        """Create a new member. If the member already exists, update the member.

        Args:
            account_id (str): The id of the account to create the member in.
            body (dict): The member to create.

        Returns:
            dict: The member.
        """
        logging.info('Creating account member')

        email = body['email'].lower()
        role = body.get('role', 'member')
        new_member = {
            'email': email,
            'role': role
        }

        # Get account
        account = self.retrieve_by_id(account_id)

        # Check if email already exists, if it does, merge body
        team = account['team']
        exists = False
        for member in team:
            if member['email'].lower() == email:
                exists = True
                member['role'] = role
        if not exists:
            team.append(new_member)

        # Update account with new team member
        data = self.collection.find_one_and_update(
            {'account': account_id},
            {'$set': {'team': team}},
            return_document=ReturnDocument.AFTER,
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def list_members(self, account_id: str) -> list:
        """List all members of an account.

        Args:
            account_id (str): The id of the account to list members of.

        Returns:
            list: The members.
        """
        logging.info('Listing members')

        account = self.retrieve_by_id(account_id)

        return account['team']

    def list_invoices(self, account_id: str) -> dict:
        """List all invoices for an account.

        Args:
            account_id (str): The id of the account to list invoices of.

        Returns:
            dict: The invoices.
        """
        logging.info('Listing invoices')
        account = self.retrieve_by_id(account_id)
        stripe_customer_id = account['billing']['stripe_customer_id']
        invoices = stripe.Invoice.list(customer=stripe_customer_id)
        return invoices

    def list_metrics(self, account_id: str, objects: str = '') -> dict:
        """List all metrics for an account.

        Args:
            account_id (str): The id of the account to list metrics of.
            objects (str): The objects to list metrics for.

        Returns:
            dict: The metrics.

        Raises:
            NotFoundError: If the objects are not valid.
        """
        logging.info('Listing metrics')
        metrics = {
            "object": "account.metrics",
            "aidrop": {},
            "claim": {},
            "collection": {},
            "contact": {},
            "journey": {},
            "journey_run": {},
            "message": {},
            "mint_link": {},
            "mint": {},
            "product": {},
            "redemption": {},
        }
        if not objects:
            return metrics
        for object in objects.split(','):
            if object == 'aidrop':
                collection = mdb[AirdropConfig.db][AirdropConfig.collection]
            elif object == 'claim':
                collection = mdb[ClaimConfig.db][ClaimConfig.collection]
            elif object == 'collection':
                collection = mdb[CollectionConfig.db][CollectionConfig.collection]
            elif object == 'contact':
                collection = mdb[ContactConfig.db][ContactConfig.collection]
            elif object == 'journey':
                collection = mdb[JourneyConfig.db][JourneyConfig.collection]
            elif object == 'journey_run':
                collection = mdb[JourneyRunConfig.db][JourneyRunConfig.collection]
            elif object == 'message':
                collection = mdb[MessageConfig.db][MessageConfig.collection]
            elif object == 'mint_link':
                collection = mdb[MintLinkConfig.db][MintLinkConfig.collection]
            elif object == 'mint':
                collection = mdb[MintConfig.db][MintConfig.collection]
            elif object == 'product':
                collection = mdb[ProductConfig.db][ProductConfig.collection]
            else:
                raise NotFoundError('Invalid object type')
            count = collection.count_documents({'account': account_id})
            metrics[object] = {'count': count}
        return metrics

    def list_subscriptions(self, account_id: str) -> dict:
        """List all subscriptions for an account.

        Args:
            account_id (str): The id of the account to list subscriptions of.

        Returns:
            dict: The subscriptions.
        """
        logging.info('Listing subscriptions')
        account = self.retrieve_by_id(account_id)
        stripe_customer_id = account['billing']['stripe_customer_id']
        subscriptions = stripe.Subscription.list(customer=stripe_customer_id)
        return subscriptions

    def create_billing_session(self, account_id: str) -> dict:
        """Create a billing session for an account.

        Args:
            account_id (str): The id of the account to create a billing session for.
            body (dict): The billing session to create.

        Returns:
            dict: The billing session.
        """
        logging.info('Creating billing')

        # Retrieve account to create billing session for
        account = self.retrieve_by_id(account_id)
        customer_id = account['billing']['stripe_customer_id']

        # Create the billing session
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=BILLING_URL
        )
        return session

    def create_checkout_session(self, account_id: str) -> dict:
        """Create a checkout session for an account.

        Args:
            account_id (str): The id of the account to create a checkout session for.
            body (dict): The checkout session to create.

        Returns:
            dict: The checkout session.
        """
        logging.info('Creating checkout')

        # Retrieve account to create checkout session for
        account = self.retrieve_by_id(account_id)
        customer_id = account['billing']['stripe_customer_id']

        # Create the checkout session
        session = stripe.checkout.Session.create(
            client_reference_id=account_id,
            customer=customer_id,
            line_items=[{
                'price': StripeConfig.STRIPE_GROWTH_PRICE,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=BILLING_URL,
            cancel_url=BILLING_URL,
        )
        logging.info(session)

        return session

    def create_token(self, account_id: str):
        """Generate a Paragon token for an account.

        Args:
            account_id (str): The id of the account to get a Paragon token for.

        Returns:
            dict: The Paragon token.
        """
        logging.info('Getting Paragon token')
        paragon = Paragon()
        token = paragon.generate_token(account_id)
        return token

    def refresh_billing_settings(self, account_id: str) -> dict:
        """Refresh billing settings for an account.

        Args:
            account_id (str): The id of the account to refresh billing settings for.

        Returns:
            dict: The account with the billing settings refreshed.
        """
        logging.info('Refreshing billing settings')

        # Retrieve account to refresh billing settings for
        account = self.retrieve_by_id(account_id)
        billing = account['billing']
        stripe_customer_id = billing['stripe_customer_id']

        # Refresh customer subscription
        subscriptions = stripe.Subscription.list(
            customer=stripe_customer_id,
            expand=['data.default_payment_method', 'data.latest_invoice'],
            status='active'
        )
        subscriptions = subscriptions['data']
        for subscription in subscriptions:
            if subscription.get('default_payment_method'):
                billing['stripe_card_brand'] = subscription['default_payment_method']['card']['brand']
                billing['stripe_card_exp_month'] = subscription['default_payment_method']['card']['exp_month']
                billing['stripe_card_exp_year'] = subscription['default_payment_method']['card']['exp_year']
                billing['stripe_card_last4'] = subscription['default_payment_method']['card']['last4']
            if subscription.get('latest_invoice'):
                billing['stripe_last_charge_amount'] = subscription['latest_invoice']['amount_due']
                billing['stripe_last_charge_at'] = subscription['latest_invoice']['created']
            if subscription.get('plan'):
                billing['stripe_plan'] = subscription['plan']['nickname']
                billing['stripe_plan_amount'] = subscription['plan']['amount']
                billing['stripe_plan_interval'] = subscription['plan']['interval']
                billing['stripe_plan_interval_count'] = subscription['plan']['interval_count']
            billing['stripe_subscription_cancel_at'] = subscription['cancel_at']
            billing['stripe_subscription_cancel_at_period_end'] = subscription['cancel_at_period_end']
            billing['stripe_subscription_period_end'] = subscription['current_period_end']
            billing['stripe_subscription_period_start'] = subscription['current_period_start']
            billing['stripe_subscription_status'] = subscription['status']

        # Update account with new team member
        data = self.collection.find_one_and_update(
            {'account': account_id},
            {'$set': {'billing': billing}},
            return_document=ReturnDocument.AFTER,
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def get_billing_summary(self, account_id: str) -> dict:
        """Get the billing summary for an account.

        Args:
            account_id (str): The id of the account to get the billing summary for.

        Returns:
            dict: The billing summary for the account.
        """
        logging.info('Getting billing summary')

        # Retrieve account to get billing summary for
        account = self.retrieve_by_id(account_id)
        billing = account['billing']
        stripe_customer_id = billing['stripe_customer_id']
        subscription_plan = billing.get('subscription_plan')
        subscription_status = billing.get('subscription_status')
        subscription_trial = billing.get('subscription_trial')

        return {
            'object': 'account.billing_summary',
            'current_period_start': 0,
            'current_period_end': 0,
            'price_base': 1000,
            'price_overage': 0,
            'price_total': 1000,
            'subscription_plan': subscription_plan,
            'subscription_status': subscription_status,
            'subscription_trial': subscription_trial,
        }
