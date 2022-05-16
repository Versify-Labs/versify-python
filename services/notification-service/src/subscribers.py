import json
import os

import mailchimp_transactional as MailchimpTransactional
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.data_classes import (EventBridgeEvent,
                                                          event_source)
from mailchimp_transactional.api_client import ApiClientError

ENV = os.environ['ENVIRONMENT']
SECRET_NAME = parameters.get_secret(os.environ['SECRET_NAME'])
SECRET = json.loads(SECRET_NAME)
MANDRILL_API_KEY = SECRET['MANDRILL_API_KEY']

tracer = Tracer()
logger = Logger()

try:
    mailchimp = MailchimpTransactional.Client(MANDRILL_API_KEY)
except ApiClientError as error:
    logger.error('An exception occurred: {}'.format(error.text))

wallet_url = 'https://wallet.versifylabs.com/'
if ENV == 'dev':
    wallet_url = 'https://wallet-dev.versifylabs.com/'


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def send_airdrop_confirmation(event, context):
    order = event.detail
    email = order.get('email', '')
    merchant_name = order['merchant_details']['display_name']
    merchant_logo = order['merchant_details']['branding']['logo_url']
    product_image = order['items'][0]['product_details']['image']
    product_name = order['items'][0]['product_details']['name']
    body = {
        'template_name': 'order-confirmation-airdrop',
        'template_content': [],
        'message': {
            'from_email': 'orders@versifylabs.com',
            'subject': 'Airdrop Received',
            'to': [
                {
                    'email': email,
                    'type': 'to'
                }
            ],
            'merge_language': 'handlebars',
            'global_merge_vars': [
                {
                    'name': 'MERCHANT_NAME',
                    'content': merchant_name
                },
                {
                    'name': 'MERCHANT_LOGO',
                    'content': merchant_logo
                },
                {
                    'name': 'PREVIEW_TEXT',
                    'content': 'Airdrop Received'
                },
                {
                    'name': 'PRODUCT_IMAGE',
                    'content': product_image
                },
                {
                    'name': 'PRODUCT_NAME',
                    'content': product_name
                },
                {
                    'name': 'WALLET_URL',
                    'content': wallet_url
                }
            ]
        }
    }
    response = mailchimp.messages.send_template(body)
    logger.info(response)
    return True
