import os
import secrets
import time

from aws_lambda_powertools import Logger, Tracer
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument

from ..api.errors import BadRequestError, NotFoundError, UsageLimitError
from ..interfaces.expandable import ExpandableResource
from ..services._config import config
from ..utils.mongo import mdb
from ..utils.stripe import Plans, stripe

logger = Logger()
tracer = Tracer()

if os.environ.get('ENVIRONMENT', 'dev') == 'prod':
    BILLING_URL = 'https://dashboard.versifylabs.com/settings/business/billing'
else:
    BILLING_URL = 'https://dashboard-dev.versifylabs.com/settings/business/billing'


class AccountService(ExpandableResource):

    def __init__(self) -> None:
        _config = config['account']
        self.collection = mdb[_config.db][_config.collection]
        self.expandables = _config.expandables
        self.Model = _config.model
        self.object = _config.object
        self.prefix = _config.prefix
        self.search_index = _config.search_index

    def create(self, body: dict) -> dict:
        """Create a new account. If the account already exists, update the account.

        Args:
            account (dict): The account to create.

        Returns:
            dict: The account.
        """
        logger.info('Creating account', extra={'body': body})

        # Create fields
        account_id = f'{self.prefix}_{ObjectId()}'
        body['_id'] = account_id
        body['account'] = account_id
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Create account name and fill into correct fields
        email = body['email'].lower()
        details = body.get('business_details', {})
        profile = body.get('business_profile', {})
        name = profile.get('name', 'Account')

        # Create basic account settings
        profile['branding'] = profile.get('branding', {})
        body['business_details'] = details
        body['business_profile'] = profile

        # Create stripe customer to bill account
        stripe_customer = stripe.Customer.create(
            description='Versify Customer',
            email=email,
            metadata={'account': account_id},
            name=name
        )

        # Construct settings object
        body['settings'] = {
            'auth': {
                'api_public_key': f'pk_{secrets.token_urlsafe(16)}',
                'api_secret_key': f'sk_{secrets.token_urlsafe(16)}'
            },
            'billing': {'stripe_customer_id': stripe_customer['id']},
            'dashboard': {'name': name},
            'team': [{'email': email, 'role': 'admin'}]
        }

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
        logger.info('Counting accounts', extra={'filter': filter})

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
        logger.info('Listing accounts', extra={'filter': filter})

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
        logger.info('Listing accounts by member email', extra={'email': email})

        # Find accounts with member matching email
        accounts = self.collection.find(filter={'settings.team.email': email})

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
        logger.info('Retrieving account', extra={'api_key': api_key})

        # Find document matching filter
        account = self.collection.find_one(
            filter={'settings.auth.api_secret_key': api_key}
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
        logger.info('Retrieving account', extra={'account_id': account_id})

        # Find document matching filter
        account = self.collection.find_one(filter={'_id': account_id})
        if not account:
            raise NotFoundError

        # Convert to JSON
        account = self.Model(**account).to_json()

        return account

    def update(self, account_id: str, update: dict) -> dict:
        """Update a account. If the account does not exist, create a new account.

        Args:
            account_id (str): The id of the account to update.
            update (dict): The fields to update.

        Returns:
            dict: The account.

        Raises:
            NotFoundError: If the account does not exist.
        """
        logger.info('Updating account', extra={'account_id': account_id})

        # Find document matching filter
        account = self.collection.find_one(filter={'_id': account_id})
        if not account:
            raise NotFoundError

        # Update fields
        account = {**account, **update}
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
        logger.info('Creating member', extra={'body': body})

        email = body['email'].lower()
        role = body.get('role', 'member')
        new_member = {
            'account': account_id,
            'email': email,
            'role': role
        }

        # Get account
        account = self.retrieve_by_id(account_id)

        # Check if email already exists, if it does, merge body
        team = account['settings']['team']
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
            {'$set': {'settings.team': team}},
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
        logger.info('Listing members', extra={'account_id': account_id})
        account = self.retrieve_by_id(account_id)
        return account['settings']['team']

    def list_invoices(self, account_id: str) -> dict:
        """List all invoices for an account.

        Args:
            account_id (str): The id of the account to list invoices of.

        Returns:
            dict: The invoices.
        """
        logger.info('Listing invoices', extra={'account_id': account_id})
        account = self.retrieve_by_id(account_id)
        stripe_customer_id = account['settings']['billing']['stripe_customer_id']
        invoices = stripe.Invoice.list(customer=stripe_customer_id)
        return invoices

    def list_subscriptions(self, account_id: str) -> dict:
        """List all subscriptions for an account.

        Args:
            account_id (str): The id of the account to list subscriptions of.

        Returns:
            dict: The subscriptions.
        """
        logger.info('Listing subscriptions', extra={'account_id': account_id})
        account = self.retrieve_by_id(account_id)
        stripe_customer_id = account['settings']['billing']['stripe_customer_id']
        subscriptions = stripe.Subscription.list(customer=stripe_customer_id)
        return subscriptions

    def reserve_mints(self, account_id: str, mint_count: int) -> dict:
        """Reserve mints for an account.

        Args:
            account_id (str): The id of the account to reserve mints for.
            mint_count (int): The number of mints to reserve.

        Returns:
            dict: The account with the mints reserved.
        """
        logger.info('Reserving mints', extra={'mint_count': mint_count})

        # Retrieve account to reserve mints for
        account = self.retrieve_by_id(account_id)

        # Check if plan requires mints to be reserved
        billing_plan = account['settings']['billing']['stripe_plan']
        if billing_plan and billing_plan.lower() in ['growth', 'enterprise']:
            return account

        # Check against usage
        trial_active = account['settings']['billing']['trial_active']
        trial_mints_available = account['settings']['billing']['trial_mints_available']
        trial_mints_reserved = account['settings']['billing']['trial_mints_reserved']
        if trial_mints_available < mint_count:
            raise UsageLimitError

        # Update billing trial mints
        trial_mints_available -= mint_count
        trial_mints_reserved += mint_count
        if trial_mints_available <= 0:
            trial_active = False

        data = self.collection.find_one_and_update(
            {'_id': account_id},
            {'$set': {
                'settings.billing.trial_active': trial_active,
                'settings.billing.trial_mints_available': trial_mints_available,
                'settings.billing.trial_mints_reserved': trial_mints_reserved
            }},
            return_document=ReturnDocument.AFTER,
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data

    def create_billing_session(self, account_id: str) -> dict:
        """Create a billing session for an account.

        Args:
            account_id (str): The id of the account to create a billing session for.
            body (dict): The billing session to create.

        Returns:
            dict: The billing session.
        """
        logger.info('Creating billing', extra={'account_id': account_id})

        # Retrieve account to create billing session for
        account = self.retrieve_by_id(account_id)
        customer_id = account['settings']['billing']['stripe_customer_id']

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
        logger.info('Creating checkout', extra={'account_id': account_id})

        # Retrieve account to create checkout session for
        account = self.retrieve_by_id(account_id)
        customer_id = account['settings']['billing']['stripe_customer_id']

        # Create the checkout session
        session = stripe.checkout.Session.create(
            client_reference_id=account_id,
            customer=customer_id,
            line_items=[{
                'price': Plans.GROWTH,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=BILLING_URL,
            cancel_url=BILLING_URL,
        )
        logger.info(session)

        return session

    def refresh_billing_settings(self, account_id: str) -> dict:
        """Refresh billing settings for an account.

        Args:
            account_id (str): The id of the account to refresh billing settings for.

        Returns:
            dict: The account with the billing settings refreshed.
        """
        logger.info('Refreshing billing settings', extra={'id': account_id})

        # Retrieve account to refresh billing settings for
        account = self.retrieve_by_id(account_id)
        billing = account['settings']['billing']
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
            {'$set': {'settings.billing': billing}},
            return_document=ReturnDocument.AFTER,
        )

        # Convert to JSON
        data = self.Model(**data).to_json()

        return data
