from aws_lambda_powertools import Logger

from ..utils.api import call_api
from ..utils.mandrill import mailchimp

logger = Logger()


class AirdropProcessor:

    def __init__(self, airdrop) -> None:
        self.airdrop = airdrop

    def validate(self):
        return True

    def get_segment(self):
        logger.info('Getting segment')
        vql = self.airdrop['recipients']['segment_options']['conditions']
        response = call_api(
            method='GET',
            path='/internal/search',
            account=self.airdrop['account'],
            params={
                'search_type': 'list_segment_contacts',
                'vql': vql
            }
        )
        logger.info(response)
        return response.get('data', [])

    def get_product(self):
        logger.info('Getting product')
        product_id = self.airdrop['product']
        product = call_api(
            method='GET',
            path=f'/internal/products/{product_id}',
            account=self.airdrop['account'],
            params={'expand': 'collection'}
        )
        logger.info(product)
        return product

    def create_mint_link(self, name, product, whitelist):
        logger.info('Creating mint link')
        mint_link = call_api(
            method='POST',
            path='/internal/mint_links',
            body={
                'airdrop': self.airdrop['id'],
                'name': name,
                'product': product,
                'public_mint': False,
                'whitelist': whitelist
            },
            account=self.airdrop['account'],
        )
        logger.info(mint_link)
        return mint_link

    def send_email(self, contact, product, mint_link):
        logger.info('Sending email')
        content = self.airdrop['email_settings'].get('content')
        from_email = self.airdrop['email_settings'].get('from_email')
        from_image = self.airdrop['email_settings'].get('from_image')
        from_name = self.airdrop['email_settings'].get('from_name')
        preview_text = self.airdrop['email_settings'].get('preview_text')
        subject_line = self.airdrop['email_settings'].get('subject_line')
        to_name = contact.get('first_name')
        greeting = 'Hi there'
        if to_name:
            greeting = 'Hi ' + to_name.capitalize()
        body = {
            'template_name': 'airdrop',
            'template_content': [],
            'message': {
                'from_email': from_email,
                'from_name': from_name,
                'subject': subject_line,
                'to': [
                    {
                        'email': contact['email'],
                        'type': 'to'
                    }
                ],
                'merge_language': 'handlebars',
                'global_merge_vars': [
                    {
                        'name': 'CLAIM_URL',
                        'content': mint_link['url']
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
                        'content': content
                    },
                    {
                        'name': 'PREVIEW_TEXT',
                        'content': preview_text
                    },
                    {
                        'name': 'PRODUCT_DESCRIPTION',
                        'content': product['description']
                    },
                    {
                        'name': 'PRODUCT_IMAGE',
                        'content': product['image']
                    },
                    {
                        'name': 'PRODUCT_NAME',
                        'content': product['name']
                    }
                ]
            }
        }
        message = mailchimp.messages.send_template(body)
        logger.info(message)
        return message

    def complete_airdrop(self):
        logger.info('Updating airdrop')
        airdrop = call_api(
            method='PUT',
            path='/internal/airdrops/' + self.airdrop['id'],
            body={'status': 'complete'},
            account=self.airdrop['account'],
        )
        logger.info(airdrop)
        return airdrop

    def start(self):
        self.validate()
        contacts = self.get_segment()
        product = self.get_product()
        name = 'Airdrop Mint Link'

        whitelist = []
        for contact in contacts:
            whitelist.append({'email': contact['email']})
        mint_link = self.create_mint_link(name, product['id'], whitelist)

        for contact in contacts:
            self.send_email(contact, product, mint_link)

        self.complete_airdrop()
        return True
