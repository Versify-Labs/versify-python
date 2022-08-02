import os
import secrets
import time

from aws_lambda_powertools import Logger
from bson.objectid import ObjectId
from pymongo.collection import ReturnDocument

from ..utils.expand import expand_object
from ..utils.mongo import mdb
from ..utils.s3 import (get_image_key, get_image_url, get_max_token_id,
                        get_metadata_key, move_s3_object,
                        upload_metadata_to_s3)
from ..utils.stripe import Plans, stripe
from ..utils.tatum import Tatum
from .config import config
from .errors import BadRequestError, NotFoundError, UsageLimitError

logger = Logger()


if os.environ.get('ENVIRONMENT', 'dev') == 'prod':
    DASHBOARD_URL = 'https://dashboard.versifylabs.com'
    METADATA_URI_BASE = "https://cdn.versifylabs.com"
    MINT_URL = 'https://mint.versifylabs.com'
else:
    DASHBOARD_URL = 'https://dashboard-dev.versifylabs.com'
    METADATA_URI_BASE = "https://cdn-dev.versifylabs.com"
    MINT_URL = 'https://mint-dev.versifylabs.com'


class ApiResource:

    def __init__(
        self,
        resource: str,
    ):
        cfg = config[resource]
        self.collection = mdb[cfg.db][cfg.collection]
        self.expandables = cfg.expandables
        self.object = cfg.object
        self.prefix = cfg.prefix or cfg.object
        self.Model = cfg.model
        self.search_index = cfg.search_index

    def count(self, filter: dict) -> int:
        return self.collection.count_documents(filter)

    def pre_create(self, body: dict, auth: dict = {}) -> dict:
        return body

    def post_create(self, body: dict, auth: dict = {}) -> dict:
        return body

    def pre_update(self, body: dict, filter: dict = {}) -> dict:
        return body

    def post_update(self, body: dict, filter: dict = {}) -> dict:
        return body

    def expand(self, data, expand_list):
        if type(data) == list:
            data = {'data': data, 'object': 'list'}
        for path in expand_list:
            if path.startswith('data'):
                new_data = []
                new_path = path[5:]
                for obj in data['data']:  # type: ignore
                    new_data.append(expand_object(obj, new_path))
                data['data'] = new_data  # type: ignore
            else:
                data = expand_object(data, path)
        return data

    def find(self, filter: dict, limit: int = 20, skip: int = 0) -> list:
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)
        return [self.Model(**doc).to_json() for doc in cursor]

    def create(self, body: dict, expand_list: list = [], auth: dict = {}) -> dict:
        logger.info('Creating object', extra={'body': body, 'auth': auth})

        # Create universal fields
        body['_id'] = body.get('_id', f'{self.prefix}_{ObjectId()}')
        body['account'] = body.get('account') or auth.get('account')
        body['created'] = int(time.time())
        body['updated'] = int(time.time())

        # Enrich payload data with object specific fields
        body = self.pre_create(body, auth)

        # Validate against schema
        data = self.Model(**body)

        # Store new item in DB
        self.collection.insert_one(data.to_bson())

        # Convert to JSON
        data = data.to_json()

        # Post processing of newly created object
        self.post_create(data, auth)

        # Expand and return data
        return self.expand(data, expand_list)  # type: ignore

    def delete(self, filter: dict) -> bool:
        logger.info('Deleting object', extra={'filter': filter})

        # Delete document matching filter
        deleted = self.collection.find_one_and_delete(filter)
        if not deleted:
            raise NotFoundError

        return True

    def get(self, filter: dict, expand_list: list = []) -> dict:
        logger.info('Getting object', extra={'filter': filter})

        # Find document matching filter
        data = self.collection.find_one(filter)
        if not data:
            raise NotFoundError

        # Convert to JSON and expand fields
        data = self.Model(**data).to_json()
        return self.expand(data, expand_list)  # type: ignore

    def list(
        self,
        filter: dict = {},
        limit: int = 20,
        skip: int = 0,
        expand_list: list = []
    ) -> list:
        logger.info('Listing objects', extra={'filter': filter})

        # Find documents matching filter
        cursor = self.collection.find(filter).sort(
            '_id', -1).limit(limit).skip(skip)

        # Convert cursor to list
        data = [self.Model(**doc).to_json() for doc in cursor]

        # Convert to JSON and expand fields
        data = self.expand(data, expand_list)  # type: ignore
        return data.get('data', [])  # type: ignore

    def update(
        self,
        body: dict,
        filter: dict,
        expand_list=[]
    ) -> dict:
        logger.info('Updating object', extra={'filter': filter})

        # Get document matching filter
        data = self.get(filter)

        # Pre processing of object being updated
        body = self.pre_update(body, filter)

        # Update data with payload
        body['updated'] = int(time.time())
        data.update(body)

        # Update document in DB
        logger.info('data', extra={'data': data})
        data = self.collection.find_one_and_update(
            filter,
            {'$set': self.Model(**data).to_bson()},
            return_document=ReturnDocument.AFTER,
        )
        logger.info('data', extra={'data': data})

        # Post processing of updated object
        self.post_update(data, filter)

        # Convert to JSON and expand fields
        data = self.Model(**data).to_json()
        return self.expand(data, expand_list)  # type: ignore


class Account(ApiResource):

    def __init__(self):
        object = 'account'
        super().__init__(object)

    def pre_create(self, body, auth={}):

        # Create account ID
        account_id = f'{self.prefix}_{ObjectId()}'
        body['_id'] = account_id
        body['account'] = account_id

        # Create account name and fill into correct fields
        email = auth.get('email')
        details = body.get('business_details', {})
        profile = body.get('business_profile', {})
        name = profile.get('name', 'Account')

        # Create basic account settings
        profile['branding'] = profile.get('branding', {})
        body['business_details'] = details
        body['business_profile'] = profile

        # Create stripe customer to bill account
        customer = stripe.Customer.create(
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
            'billing': {'customer': customer},
            'dashboard': {'name': name},
            'team': [{'email': email, 'role': 'admin'}]
        }
        return body

    def create_member(self, body: dict, expand_list: list = [], auth: dict = {}) -> dict:
        logger.info('Creating team member')
        account_id = auth.get('account')
        email = body['email'].lower()
        role = body.get('role', 'member')

        # Get account
        account = self.get(filter={'account': account_id})

        # Check if email already exists, if it does, merge body
        team = account['settings']['team']
        exists = False
        for member in team:
            logger.info('Member', extra={'member': member})
            if member['email'].lower() == email:
                exists = True
                member['role'] = role
        if not exists:
            team.append({'email': email, 'role': role})

        # Update account with new team member
        account = self.collection.find_one_and_update(
            {'account': account_id},
            {'$set': {"settings.team": team}},
            return_document=ReturnDocument.AFTER,
        )
        logger.info('Updated account', extra={'account': account})

        return account

    def create_subscription(self, body: dict, expand_list: list = [], auth: dict = {}) -> dict:
        logger.info('Creating subscription')
        account_id = auth.get('account')
        payment_method_id = body['payment_method']
        plan = body['plan']
        if plan == 'basic':
            price_id = Plans.BASIC
        elif plan == 'growth':
            price_id = Plans.GROWTH
        else:
            raise BadRequestError('Invalid plan')

        # Get account
        account = self.get(filter={'account': account_id})

        # Get customer
        customer = account['settings']['billing']['customer']
        customer_id = customer['id']

        # Attach the payment method to the customer
        stripe.PaymentMethod.attach(
            payment_method_id,
            customer=customer_id,
        )

        # Set the default payment method on the customer
        stripe.Customer.modify(
            customer_id,
            invoice_settings={'default_payment_method': payment_method_id},
        )

        # Create the subscription
        subscription = stripe.Subscription.create(
            customer=customer_id,
            items=[{'price': price_id}],
            expand=['latest_invoice.payment_intent'],
        )
        logger.info(subscription)
        return subscription

    def update_subscription(self, subscription_id, body: dict) -> dict:
        logger.info('Updating subscription')
        plan = body['plan']
        if plan == 'basic':
            price_id = Plans.BASIC
        elif plan == 'growth':
            price_id = Plans.GROWTH
        else:
            raise BadRequestError('Invalid plan')

        # Get the current subscription
        subscription = stripe.Subscription.retrieve(subscription_id)
        logger.info(subscription)

        # Update the subscription
        new_items = []
        for item in subscription['items']['data']:
            logger.info('Item:')
            logger.info(item)

            # Update the item to the new plans price
            if item['price']['nickname'] in ['Basic', 'Growth']:
                new_items.append(
                    {
                        'id': item.id,
                        'price': price_id
                    }
                )

        subscription = stripe.Subscription.modify(
            subscription_id,
            cancel_at_period_end=False,
            items=new_items
        )
        logger.info(subscription)
        return subscription


class Airdrop(ApiResource):

    def __init__(self):
        object = 'airdrop'
        super().__init__(object)

    def pre_create(self, body, auth={}):
        account = Account().get({'account': body['account']})
        business_profile = account['business_profile']
        business_branding = business_profile['branding']
        body['recipients'] = body.get('recipients') or {}
        body['email_settings']['from_email'] = business_branding.get('logo')
        body['email_settings']['from_image'] = business_branding.get('logo')
        body['email_settings']['from_name'] = business_profile.get('name')
        return body


class Collection(ApiResource):

    def __init__(self):
        object = 'collection'
        super().__init__(object)

    def deploy(self, id, expand_list=[]):
        """Deploy ERC1155 smart contract for the collection

        Args:
            id (str): ID of the collection

        Returns:
            collection (dict): Updated collection
        """

        # Deploy ERC1155 smart contract for the collection
        tatum = Tatum()
        token_uri = f"{METADATA_URI_BASE}/products/{id}" + "/{id}.json"
        response = tatum.deploy_contract(token_uri)
        logger.info(response)
        signature = response.get('signatureId')

        # Update body with signature and uri
        updates = {'uri': token_uri}
        filter = {'_id': id}
        if signature:
            updates['signature'] = signature
            updates['status'] = 'pending'
            return super().update(updates, filter, expand_list)
        else:
            updates['status'] = 'failed'
            super().update(updates, filter, expand_list)
            logger.error('Could not deploy contract')
            logger.error(response)
            raise RuntimeError

    def pre_create(self, body: dict, auth: dict = {}) -> dict:

        # TODO: Validate against billing usage
        within_usage_limit = True
        if not within_usage_limit:
            raise UsageLimitError

        return body

    def post_create(self, body: dict, auth: dict = {}) -> dict:
        logger.info('Created collection', extra={'collection': body})
        collection_id = body['id']

        # Return collection after contract is deployed
        return self.deploy(collection_id, [])

    def pre_update(self, body: dict, filter: dict = {}) -> dict:

        # Add minter role for Versify KMS Wallet
        if body.get('contract_address'):
            tatum = Tatum()
            contract_address = body.get('contract_address')
            try:
                result = tatum.add_minter(contract_address)
                logger.info(result)
            except Exception as err:
                logger.error(err)

        return super().pre_update(body, filter)


class Contact(ApiResource):

    def __init__(self):
        object = 'contact'
        super().__init__(object)

    def upsert(self, body, expand_list, auth):
        """Check if email exists. If yes, merge with existing contact"""

        filter = {
            'email': body['email'],
            'account': auth['account']
        }
        existing_contacts = self.list(filter)
        logger.info(existing_contacts)

        if len(existing_contacts) > 0:
            existing_contact = existing_contacts[0]
            filter['_id'] = existing_contact['id']
            return super().update(body, filter, expand_list)
        else:
            return super().create(body, expand_list, auth)

    def create(self, body, expand_list, auth):
        return self.upsert(body, expand_list, auth)


class Event(ApiResource):

    def __init__(self):
        object = 'event'
        super().__init__(object)


class MintLink(ApiResource):

    def __init__(self):
        object = 'mint_link'
        super().__init__(object)

    def pre_create(self, body, auth={}):
        account = Account().get({'account': body['account']})
        business_branding = account['business_profile']['branding']
        body['branding'] = {
            'colors': {
                'background': business_branding['primary_color'],
                'button': business_branding['secondary_color']
            },
            'logo': business_branding.get('logo'),
            'name': account['business_profile']['name']
        }
        body['url'] = MINT_URL + '/' + body['_id']
        return body


class Mint(ApiResource):

    def __init__(self):
        object = 'mint'
        super().__init__(object)

    def pre_create(self, body: dict, auth: dict = {}) -> dict:
        account = None
        email = body.get('email')

        if body.get('airdrop'):
            airdrop_id = body['airdrop']
            airdrop = Airdrop().get({'_id': airdrop_id})
            account = airdrop['account']

        if body.get('mint_link'):
            mint_link_id = body['mint_link']
            mint_link = MintLink().get({'_id': mint_link_id})
            account = mint_link['account']

            # If mint link is not public, we need to check whitelist
            if not mint_link.get('public_mint', True):
                email_allowed = False
                whitelist = mint_link.get('whitelist', [])
                for i, spot in enumerate(whitelist):
                    if spot['email'] == email and spot['status'] != 'claimed':
                        email_allowed = True
                        whitelist[i] = {'email': email, 'status': 'claimed'}
                        break
                if email_allowed:
                    MintLink().update(
                        body={'whitelist': whitelist},
                        filter={'_id': mint_link_id}
                    )
                else:
                    err = 'Email is not authorized to mint'
                    raise BadRequestError(err)

        body['account'] = account
        return body

    def post_create(self, body: dict, auth: dict = {}) -> dict:

        if body.get('wallet_address'):
            return self.fulfill(body, filter={'_id': body['id']})

        return body

    def fulfill(
        self,
        body: dict,
        filter: dict,
        expand_list=[]
    ) -> dict:
        logger.info('Fulfilling mint', extra={'filter': filter})

        # Get the mint, product, and collection
        mint = self.get(filter, expand_list=['product.collection'])
        product = mint['product']
        collection = product['collection']

        # Mint token to contract
        tatum = Tatum()
        response = tatum.mint_token(
            contract=collection['contract_address'],
            token=product['token_id'],
            to=body['wallet_address']
        )
        logger.info(response)
        signature = response.get('signatureId')

        # Update body with signature
        updates = {}
        if signature:
            updates['signature'] = signature
            updates['status'] = 'pending'
            return super().update(updates, filter, expand_list)
        else:
            updates['status'] = 'failed'
            super().update(updates, filter, expand_list)
            logger.error('Could not mint token')
            logger.error(response)
            raise RuntimeError


class Note(ApiResource):

    def __init__(self):
        object = 'note'
        super().__init__(object)


class Product(ApiResource):

    def __init__(self):
        object = 'product'
        super().__init__(object)

    def to_hex(self, x):
        x = int(x)
        padding = 4
        return f"{x:#0{padding}x}"

    def upsert_metadata(self, product):

        # Check product data to see what we need to do
        collection_id = product['collection']
        contract_address = product['contract_address']
        token_id = product.get('token_id')

        # Create token_id if it doesn't exist
        if not token_id:
            max_token_id = get_max_token_id(collection_id)
            token_id = max_token_id + 1
        product['token_id'] = token_id
        token_id_hex = self.to_hex(token_id)

        # Move product image from /tmp to /metadata/collection_id/token_id
        old_key = '/'.join(product['image'].split('/')[-2:])
        metadata_key_dec = get_metadata_key(collection_id, token_id)
        metadata_key_hex = get_metadata_key(collection_id, token_id_hex)
        image_key = get_image_key(collection_id, token_id_hex)
        image_url = get_image_url(collection_id, token_id_hex)
        move_s3_object(old_key, image_key)

        # Upload metadata
        metadata = {
            'name': product['name'],
            'description': product['description'],
            'image': image_url,
            "attributes": product.get('properties', []),
            'external_url': f'https://market.versifylabs.com/{contract_address}/{token_id}',
            # 'animation_url': '',
            # 'youtube_url': ''
        }

        metadata['external_url'] = 'https://market.versifylabs.com'
        metadata.update({
            'external_url': 'https://versifylabs.com',
            # 'animation_url': '',
            # 'youtube_url': ''
        })
        upload_metadata_to_s3(metadata_key_dec, metadata)
        upload_metadata_to_s3(metadata_key_hex, metadata)

        return product

    def pre_create(self, body, auth={}):

        # Validate that the collection has been deployed
        collection_id = body['collection']
        collection = Collection().get(filter={'_id': collection_id})
        if collection.get('status', 'pending') != 'deployed':
            raise BadRequestError('Collection must be deployed.')
        body['chain'] = collection.get('chain', 'polygon')
        body['contract_address'] = collection['contract_address']

        # Upload metadata to S3
        body = self.upsert_metadata(product=body)

        return body

    def update(self, body, filter, expand_list):

        # Update product in DB
        product = super().update(body, filter, expand_list)

        # Upload metadata to S3
        self.upsert_metadata(product=product)

        return product


class Signature:

    def __init__(self):
        self.object = 'signature'

    def exists(self, id: str):

        # Add signature id to query
        params = {'signature': id}

        # Check collections
        resource = Collection()
        collections = resource.list(params)

        # Check mints
        resource = Mint()
        mints = resource.list(params)

        if len(collections) + len(mints) > 0:
            return True
        raise NotFoundError


class User(ApiResource):

    def __init__(self):
        object = 'user'
        super().__init__(object)

    def get_user_filter(self, id, email, stytch_user):
        expressions = []
        if id:
            expressions.append({'_id': id})
        if email:
            expressions.append({'email': email})
        if stytch_user:
            expressions.append({'stytch_user': stytch_user})
        if not expressions:
            return {}
        return {'$or': expressions}

    def list_accounts(self, email):
        logger.info('Listing accounts', extra={'email': email})

        accounts = Account().list(filter={'settings.team.email': email})
        logger.info(accounts)

        return accounts

    def create(self, body: dict, expand_list: list = [], auth: dict = {}) -> dict:
        logger.info('Creating object', extra={'body': body, 'auth': auth})
        id = body.get('id')
        email = body.get('email')
        stytch_user = body.get('stytch_user')

        user = None
        try:
            user_filter = self.get_user_filter(id, email, stytch_user)
            user = self.get(filter=user_filter)
            logger.info('User exists. Updating...')

            # Update user with any new data
            needs_update = False
            for k, v in body.items():
                if user.get(k) != v:
                    needs_update = True
            if needs_update:
                user = self.update(body, filter=user_filter)

        except NotFoundError:
            logger.info('User does not exist. Creating...')

            # Create universal fields
            body['_id'] = f'{self.prefix}_{ObjectId()}'
            body['created'] = int(time.time())
            body['updated'] = int(time.time())

            # Enrich payload data with object specific fields
            body = self.pre_create(body, auth)

            # Validate against schema
            data = self.Model(**body)

            # Store new item in DB
            self.collection.insert_one(data.to_bson())

            # Convert to JSON
            user = data.to_json()

            # Post processing of newly created object
            user = self.post_create(user, auth)

        # Expand user accounts
        accounts = self.list_accounts(email)
        user['accounts'] = accounts

        # Return data
        return user


class Webhook(ApiResource):

    def __init__(self):
        object = 'webhook'
        super().__init__(object)


class Versify(object):
    """Provides easy access to all resource classes"""

    def __init__(self):
        self.account = Account()
        self.airdrop = Airdrop()
        self.collection = Collection()
        self.contact = Contact()
        self.event = Event()
        self.mint_link = MintLink()
        self.mint = Mint()
        self.note = Note()
        self.product = Product()
        self.user = User()
        self.webhook = Webhook()
