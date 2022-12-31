from typing import Any, Dict, List, Optional

from app.db.session import SessionLocal
from app.models.account import Account
from app.models.contact import Contact
from app.models.user import User
from pymongo import ReturnDocument
from pymongo.collection import Collection


class Versify:
    def __init__(self) -> None:
        self.session = SessionLocal()

        # Initialize collections
        db_name = "Dev"
        self.accounts = self.session.get_collection(db_name, "Accounts")
        self.contacts = self.session.get_collection(db_name, "Contacts")
        self.users = self.session.get_collection(db_name, "Users")

    def _update(
        self, collection: Collection, id: str, body: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        updates = {}
        for key, value in body.items():
            if value is not None:
                updates[key] = value
        if not updates or len(updates) <= 1:
            return None
        return collection.find_one_and_update(
            filter={"_id": id},
            update={"$set": updates},
            return_document=ReturnDocument.AFTER,
        )

    def create_user(self, body: Dict[str, Any] = {}) -> User:
        user_body = User(**body)
        self.users.insert_one(user_body.bson())
        return user_body

    def list_users(self, filter: Dict[str, Any] = {}) -> List[User]:
        users = self.users.find(filter)
        return [User(**user) for user in users]

    def get_user(self, filter: Dict[str, Any] = {}) -> Optional[User]:
        user = self.users.find_one(filter)
        return User(**user) if user is not None else None

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.get_user({"_id": user_id})

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.get_user({"email": email})

    def update_user(self, user_id: str, body: Dict[str, Any] = {}) -> Optional[User]:
        user = self._update(self.users, user_id, body)
        return User(**user) if user is not None else None

    def delete_user(self, user_id: str) -> bool:
        deleted = self.users.delete_one({"_id": user_id})
        return deleted.deleted_count == 1

    def create_account(self, body: Dict[str, Any] = {}) -> Account:
        account_body = Account(**body)
        self.accounts.insert_one(account_body.bson())
        return account_body

    def list_accounts(self, filter: Dict[str, Any] = {}) -> List[Account]:
        accounts = self.accounts.find(filter)
        return [Account(**account) for account in accounts]

    def list_accounts_by_email(self, email: str) -> List[Account]:
        return self.list_accounts({"team.email": email})

    def get_account(self, filter: Dict[str, Any] = {}) -> Optional[Account]:
        account = self.accounts.find_one(filter)
        return Account(**account) if account is not None else None

    def get_account_by_id(self, account_id: str) -> Optional[Account]:
        return self.get_account({"_id": account_id})

    def update_account(
        self, account_id: str, body: Dict[str, Any] = {}
    ) -> Optional[Account]:
        account = self._update(self.accounts, account_id, body)
        return Account(**account) if account is not None else None

    def delete_account(self, account_id: str) -> bool:
        deleted = self.accounts.delete_one({"_id": account_id})
        return deleted.deleted_count == 1

    def create_contact(self, body: Dict[str, Any] = {}) -> Contact:
        contact_body = Contact(**body)
        self.contacts.insert_one(contact_body.bson())
        return contact_body

    def list_contacts(self, filter: Dict[str, Any] = {}) -> List[Contact]:
        contacts = self.contacts.find(filter)
        return [Contact(**contact) for contact in contacts]

    def get_contact(self, filter: Dict[str, Any] = {}) -> Optional[Contact]:
        contact = self.contacts.find_one(filter)
        return Contact(**contact) if contact is not None else None

    def get_contact_by_id(self, contact_id: str) -> Optional[Contact]:
        return self.get_contact({"_id": contact_id})

    def update_contact(
        self, contact_id: str, body: Dict[str, Any] = {}
    ) -> Optional[Contact]:
        contact = self._update(self.contacts, contact_id, body)
        return Contact(**contact) if contact is not None else None

    def delete_contact(self, contact_id: str) -> bool:
        deleted = self.contacts.delete_one({"_id": contact_id})
        return deleted.deleted_count == 1
