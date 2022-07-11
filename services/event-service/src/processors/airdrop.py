from aws_lambda_powertools import Logger

from ..utils.api import call_api

logger = Logger()


class AirdropProcessor:

    def __init__(self, airdrop) -> None:
        self.airdrop = airdrop

    def validate(self):
        return True

    def get_organization(self):
        org_id = self.airdrop['organization']
        organization = call_api(
            method='GET',
            path=f'/partners/auth0/organizations/{org_id}/validate',
            organization=self.airdrop['organization']
        )
        logger.info(organization)
        return organization

    def get_product(self):
        product_id = self.airdrop['product']
        product = call_api(
            method='GET',
            path=f'/internal/products/{product_id}',
            organization=self.airdrop['organization'],
            params={'expand': 'collection'}
        )
        logger.info(product)
        return product

    def get_segment(self):
        vql = self.airdrop['recipients']['segment_options']['conditions']
        response = call_api(
            method='GET',
            path='/internal/contacts/aggregate/segment',
            organization=self.airdrop['organization'],
            params={'vql': vql}
        )
        logger.info(response)
        return response.get('data', [])

    def create_mint(self, contact, product):
        logger.info('Creating mint')
        mint = call_api(
            method='POST',
            path='/internal/mints',
            body={
                'airdrop': self.airdrop['id'],
                'contact': contact['id'],
                'product': self.airdrop['product']
            },
            organization=self.airdrop['organization'],
        )
        logger.info(mint)
        return mint

    def send_email(self, contact, product, mint):
        logger.info('Sending email')
        content = self.airdrop['email_settings']['content']
        from_email = self.airdrop['email_settings']['from_email']
        from_image = self.airdrop['email_settings']['from_image']
        from_name = self.airdrop['email_settings']['from_name']
        preview_text = self.airdrop['email_settings']['preview_text']
        subject_line = self.airdrop['email_settings']['subject_line']
        to_name = contact.get('first_name')
        greeting = 'Hi there'
        if to_name:
            greeting = 'Hi ' + to_name.capitalize()
        message = call_api(
            method='POST',
            path='/partners/mandrill/messages',
            body={
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
                            'content': mint['url']
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
            },
            organization=self.airdrop['organization'],
        )
        logger.info(message)
        return message

    def update_airdrop(self):
        logger.info('Updating airdrop')
        airdrop = call_api(
            method='PUT',
            path='/internal/airdrops/' + self.airdrop['id'],
            body={
                'status': 'complete'
            },
            organization=self.airdrop['organization'],
        )
        logger.info(airdrop)
        return airdrop

    def start(self):
        self.validate()
        contacts = self.get_segment()
        product = self.get_product()
        for contact in contacts:
            mint = self.create_mint(contact, product)
            self.send_email(contact, product, mint)
        self.update_airdrop()
        return True
