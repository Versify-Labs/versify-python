from pynamodb.exceptions import DoesNotExist
from versify.utilities.model import generate_uuid

from .model import Customer as CustomerModel


class Customers:

    def __init__(self, organization: str):
        self.model = CustomerModel
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

    def to_list(self, items):
        return [item.to_dict() for item in items]

    def create(self, body: dict = {}, raw: bool = True):
        """Create a new customer"""
        id = generate_uuid('customer')
        body['PK'] = id
        body['SK'] = id
        body['id'] = id
        body['organization'] = self.organization
        body['first_name'] = self.get_first_name(body)
        body['last_name'] = self.get_last_name(body)
        customer = self.model(**body)
        customer.save()
        return customer.to_dict() if raw else customer

    def list(self, query: dict = {}, raw: bool = True):
        """Retrieves an customer by its id"""
        customers = self.model.by_organization_by_object.query(
            hash_key=self.organization,
            range_key_condition=self.model.object == 'customer'
        )
        return self.to_list(customers) if raw else customers

    def get(self, id: str, raw: bool = True):
        """Retrieves an customer by its id"""
        try:
            item = self.model.get(id, id)
        except DoesNotExist:
            return None
        return item.to_dict() if raw else item

    def update(self, id: str, body: dict = {}, raw: bool = True):
        """Update an existing customer"""
        customer = self.get(id, raw=False)
        actions = []
        for k, v in body.items():
            attr = getattr(self.model, k)
            actions.append(attr.set(v))
        print(actions)
        customer.update(actions=actions)
        return customer.to_dict() if raw else customer

    def update_with_order(self, order: dict):
        """Update custuomer with order data"""
        customer_id = order['customer']
        currency = order['amount_currency']
        order_total = order['amount_total']
        customer = self.get(customer_id, raw=False)
        customer.update(actions=[
            self.model.currency.set(currency),
            self.model.total_orders.set(customer.total_orders + 1),
            self.model.total_spent.set(customer.total_spent + order_total)
        ])
        return True


class Versify:

    def __init__(self, organization: str) -> None:
        self.customers = Customers(organization)
