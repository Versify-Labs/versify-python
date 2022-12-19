import json
import os

import mailchimp_transactional as MailchimpTransactional
from aws_lambda_powertools import Logger  # type: ignore
from aws_lambda_powertools.utilities import parameters
from mailchimp_transactional.api_client import ApiClientError

ENV = os.environ['ENVIRONMENT']
SECRET_NAME = parameters.get_secret(os.environ['SECRET_NAME'])
SECRET = json.loads(SECRET_NAME)
MANDRILL_API_KEY = SECRET['MANDRILL_API_KEY']

logger = Logger()

try:
    mailchimp = MailchimpTransactional.Client(MANDRILL_API_KEY)
except ApiClientError as error:
    logger.error('An exception occurred: {}'.format(error.text))
