import logging

import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

from ..config import MandrillConfig

try:
    api_key = MandrillConfig.MANDRILL_API_KEY
    mailchimp = MailchimpTransactional.Client(api_key)
except ApiClientError as error:
    logging.error("An exception occurred: {}".format(error.text))
