from functools import total_ordering
import time

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.event_handler.exceptions import BadRequestError
from pynamodb.exceptions import DoesNotExist
from versify.utilities.model import generate_uuid

from .model import Contact as ContactModel
from .model import Note as NoteModel
from .model import Tag as TagModel

tracer = Tracer()
logger = Logger()
app = APIGatewayRestResolver()


class Contacts:

    def __init__(self, organization: str):
        self.model = ContactModel
        self.organization = organization

    def get_first_name(self, body):
        try:
            if body.get('first_name'):
                return body['first_name']
            if body.get('name'):
                return body['name'].split(' ')[0]
        except:
            return ''

    def get_last_name(self, body):
        try:
            if body.get('last_name'):
                return body['last_name']
            if body.get('name'):
                return body['name'].split(' ')[1]
        except:
            return ''

    def get_filter_condition(self, options):

        # Handle View
        view_condition = None
        view = options.get('view', 'all')
        if view == 'archived':
            view_condition = self.model.archived == True
        else:
            view_condition = self.model.archived == False
        condition = view_condition

        # Handle Query
        query_condition = None
        query_attrs = ['email', 'name', 'first_name', 'last_name']
        query = options.get('query', '')
        for attr in query_attrs:
            if query_condition != None:
                query_condition |= getattr(self.model, attr).contains(query)
            else:
                query_condition = getattr(self.model, attr).contains(query)
        if query_condition != None:
            condition &= query_condition

        # Handle Filter
        filters_condition = None
        filters = options.get('filters', '').split(',')
        filters = [f for f in filters if f.count('-') == 2]
        for f in filters:
            prop, op, val = f.split('-')
            f_condition = None
            if op == 'equal':
                f_condition = getattr(self.model, prop) == val
            elif op == 'notEqual':
                f_condition = getattr(self.model, prop) != val
            elif op == 'contains':
                f_condition = getattr(self.model, prop).contains(val)
            elif op == 'notContains':
                f_condition = ~getattr(self.model, prop).contains(val)
            elif op == 'startsWith':
                f_condition = getattr(self.model, prop).startswith(val)
            elif op == 'greaterThan':
                f_condition = getattr(self.model, prop) > val
            elif op == 'lessThan':
                f_condition = getattr(self.model, prop) < val
            elif op == 'isBlank':
                f_condition = getattr(self.model, prop).does_not_exist()
            elif op == 'isPresent':
                f_condition = getattr(self.model, prop).exists()
            if f_condition != None:
                if filters_condition != None:
                    filters_condition &= f_condition
                else:
                    filters_condition = f_condition
        if filters_condition != None:
            condition &= filters_condition

        logger.info(condition)
        return condition

    def to_list(self, items):
        return [item.to_dict() for item in items]

    def create(self, body: dict = {}, raw: bool = True):
        """Create a new contact"""
        contact_id = generate_uuid('contact')
        timestamp = int(time.time())
        body['PK'] = f'{self.organization}:contact'
        body['id'] = contact_id
        body['date_created'] = timestamp
        body['date_updated'] = timestamp
        body['first_name'] = self.get_first_name(body)
        body['last_name'] = self.get_last_name(body)
        body['organization'] = self.organization
        contact = self.model(**body)
        contact.save()
        return contact.to_dict() if raw else contact

    def list(self, query_params: dict = {}, raw: bool = True):
        """Retrieves a list of contacts for the org"""
        logger.info(query_params)
        filter_condition = self.get_filter_condition(query_params)
        limit = query_params.get('limit', 20)
        before = int(query_params.get(
            'starting_before', 10000000000000000000)) - 1
        after = int(query_params.get('starting_after', 0)) + 1
        contacts = self.model.by_organization.query(
            hash_key=f'{self.organization}:contact',
            range_key_condition=self.model.date_created.between(after, before),
            filter_condition=filter_condition,
            limit=limit,
            scan_index_forward=False
        )
        return self.to_list(contacts) if raw else contacts

    def get(self, id: str, raw: bool = True):
        """Retrieves a contact by its id"""
        try:
            item = self.model.get(f'{self.organization}:contact', id)
        except DoesNotExist:
            return None
        return item.to_dict() if raw else item

    def update(self, id: str, body: dict = {}, raw: bool = True):
        """Update an existing contact"""
        contact = self.get(id, raw=False)
        actions = [self.model.date_updated.set(int(time.time()))]
        for k, v in body.items():
            attr = getattr(self.model, k)
            actions.append(attr.set(v))
        contact.update(actions=actions)
        return contact.to_dict() if raw else contact

    def delete(self, contact_id: str):
        """Delete a contact"""
        contact = self.get(contact_id, raw=False)
        contact.delete()
        return id

    def archive(self, contact_id: str):
        """Archive a contact"""
        body = {'archived': True}
        contact = self.update(contact_id, body)
        return contact

    def unarchive(self, contact_id: str):
        """Unarchives a contact"""
        body = {'archived': False}
        contact = self.update(contact_id, body)
        return contact

    def add_airdrop(self, contact_id: str, quantity: int = 1):
        """Add airdrop to a contacts stats"""
        contact = self.get(contact_id, raw=False)
        contact_dict = contact.to_dict()
        total_airdrops = contact_dict.get('total_airdrops', 0) + quantity
        body = {'total_airdrops': total_airdrops}
        contact = self.update(contact_id, body)
        return contact

    def update_with_order(self, order: dict):
        """Update contact with order data"""
        contact_id = order['contact']
        currency = order['amount_currency']
        order_total = order['amount_total']
        contact = self.get(contact_id, raw=False)
        body = {
            'currency': currency,
            'total_orders': contact.total_orders + 1,
            'total_spent': contact.total_spent + order_total
        }
        contact = self.update(contact_id, body)
        return contact


class Notes:

    def __init__(self, organization: str):
        self.model = NoteModel
        self.organization = organization

    def to_list(self, items):
        return [item.to_dict() for item in items]

    def create(self, contact_id, body: dict = {}, raw: bool = True):
        """Create a new note"""
        note_id = generate_uuid('note')
        timestamp = int(time.time())
        body['PK'] = f'{contact_id}:note'
        body['id'] = note_id
        body['contact'] = contact_id
        body['date_created'] = timestamp
        body['date_updated'] = timestamp
        body['organization'] = self.organization
        note = self.model(**body)
        note.save()
        return note.to_dict() if raw else note

    def list_by_contact(self, contact_id: str, raw: bool = True):
        """Retrieves a list of notes by a contact"""
        notes = self.model.by_contact.query(
            hash_key=f'{contact_id}:note'
        )
        return self.to_list(notes) if raw else notes

    def get(self, contact_id: str, note_id: str, raw: bool = True):
        """Retrieve a note by its id"""
        try:
            item = self.model.get(f'{contact_id}:note', note_id)
        except DoesNotExist:
            return None
        return item.to_dict() if raw else item

    def delete(self, contact_id, note_id: str):
        """Delete a note"""
        note = self.get(contact_id, note_id, raw=False)
        note.delete()
        return id


class Tags:

    def __init__(self, organization: str):
        self.model = TagModel
        self.organization = organization

    def to_list(self, items):
        return [item.to_dict() for item in items]

    def create(self, body: dict = {}, contact_id=None, raw: bool = True):
        """Create a new tag"""
        tag = None

        tag_name = body['name'].lower()
        timestamp = int(time.time())
        body['id'] = f'tag_{tag_name}'
        body['contact'] = contact_id
        body['date_created'] = timestamp
        body['date_updated'] = timestamp
        body['name'] = tag_name
        body['organization'] = self.organization

        #  Create tag for contact
        if contact_id:
            body['PK'] = f'{contact_id}:tag'
            tag = self.model(**body)
            tag.save()

        # Create tag for org if it doesnt exist
        if not self.get(tag_id=f'tag_{tag_name}'):
            body['PK'] = f'{self.organization}:tag'
            tag = self.model(**body)
            tag.save()

        if tag:
            return tag.to_dict() if raw else tag
        else:
            return None

    def list_by_org(self, raw: bool = True):
        """Retrieves a list of tags by an org"""
        tags = self.model.by_organization.query(
            hash_key=f'{self.organization}:tag'
        )
        return self.to_list(tags) if raw else tags

    def list_by_contact(self, contact_id: str, raw: bool = True):
        """Retrieves a list of tags for a contact"""
        tags = self.model.by_contact.query(
            hash_key=f'{contact_id}:tag'
        )
        return self.to_list(tags) if raw else tags

    def get(self, tag_id: str, raw: bool = True):
        """Retrieve a tag by its id"""
        try:
            item = self.model.get(f'{self.organization}:tag', tag_id)
        except DoesNotExist:
            return None
        return item.to_dict() if raw else item


class Versify:

    def __init__(self, organization: str) -> None:
        self.contacts = Contacts(organization)
        self.notes = Notes(organization)
        self.tags = Tags(organization)
