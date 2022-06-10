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


@event_source(data_class=EventBridgeEvent)
@logger.inject_lambda_context(log_event=True)
@tracer.capture_lambda_handler
def send_airdrop_notification(event, context):
    airdrop = event.detail
    campaign = airdrop['campaign_details']
    product = airdrop['product_details']

    to_email = airdrop['contact_details']['email']
    to_name = airdrop['contact_details'].get('first_name')
    greeting = 'Hi there'
    if to_name:
        greeting = 'Hi ' + to_name.capitalize()

    subject_line = campaign['email_settings']['subject_line']
    preview_text = campaign['email_settings']['preview_text']

    from_name = campaign['email_settings']['from_name']
    from_image = campaign['email_settings']['from_image']

    product_description = product['description']
    product_name = product['name']
    product_image = product['image']

    message = campaign['email_settings']['content']
    claim_url = airdrop['mint_details']['link']

    body = {
        'template_name': 'airdrop',
        'template_content': [],
        'message': {
            'from_email': 'claims@versifylabs.com',
            'from_name': from_name,
            'subject': subject_line,
            'to': [
                {
                    'email': to_email,
                    'type': 'to'
                }
            ],
            'merge_language': 'handlebars',
            'global_merge_vars': [
                {
                    'name': 'CLAIM_URL',
                    'content': claim_url
                },
                {
                    'name': 'FROM_NAME',
                    'content': from_name
                },
                {
                    'name': 'FROM_IMAGE',
                    'content': from_image
                },
                {
                    'name': 'GREETING',
                    'content': greeting
                },
                {
                    'name': 'MESSAGE',
                    'content': message
                },
                {
                    'name': 'PREVIEW_TEXT',
                    'content': preview_text
                },
                {
                    'name': 'PRODUCT_DESCRIPTION',
                    'content': product_description
                },
                {
                    'name': 'PRODUCT_IMAGE',
                    'content': product_image
                },
                {
                    'name': 'PRODUCT_NAME',
                    'content': product_name
                }
            ]
        }
    }
    response = mailchimp.messages.send_template(body)
    logger.info(response)
    return True
