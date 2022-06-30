import json
import os

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities import parameters

import stripe

SECRET_RAW = parameters.get_secret(os.environ['SECRET_NAME'])
SECRET = json.loads(SECRET_RAW)
STRIPE_SECRET_KEY = SECRET['STRIPE_SECRET_KEY']
STRIPE_PUBLIC_KEY = SECRET['STRIPE_PUBLIC_KEY']
STRIPE_WEBHOOK_SECRET = SECRET['STRIPE_WEBHOOK_SECRET']

logger = Logger()


class Keys:
    SECRET = STRIPE_SECRET_KEY
    PUBLIC = STRIPE_PUBLIC_KEY
    WEBHOOK = STRIPE_WEBHOOK_SECRET


class BasicPackage:
    PACKAGE_PRICE = os.environ['STRIPE_BASIC_PACKAGE_PRICE']
    COLLECTION_PRICE = os.environ['STRIPE_BASIC_COLLECTION_PRICE']
    MINT_PRICE = os.environ['STRIPE_BASIC_MINT_PRICE']


class GrowthPackage:
    PACKAGE_PRICE = os.environ['STRIPE_GROWTH_PACKAGE_PRICE']
    COLLECTION_PRICE = os.environ['STRIPE_GROWTH_COLLECTION_PRICE']
    MINT_PRICE = os.environ['STRIPE_GROWTH_MINT_PRICE']


stripe.api_key = Keys.SECRET
