from app.api.deps import identity_with_account
from app.crud import versify
from app.api.models import (
    ApiDeleteResponse,
    ApiListResponse,
    ApiSearchResponse,
    BodyParams,
    Identity,
    PathParams,
    QueryParams,
    SearchQuery,
)
from app.models.contact import Contact, ContactCreate, ContactUpdate

from app.models.enums import TeamMemberRole
from app.api.exceptions import ForbiddenException, NotFoundException
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.get(
    path="",
    summary="List contacts",
    description="List contacts with optional filters and pagination parameters",
    tags=["Contacts"],
    status_code=200,
    response_model=ApiListResponse,
    response_description="The list of contacts",
)
def list_contacts(
    identity: Identity = Depends(identity_with_account),
    page_num: int = QueryParams.PAGE_NUM,
    page_size: int = QueryParams.PAGE_SIZE,
    collection: str = QueryParams.COLLECTION_ID,
    status: str = QueryParams.COLLECTION_STATUS,
):
    if identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.contacts.count(
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    contacts = versify.contacts.list(
        page_num=page_num,
        page_size=page_size,
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    return {"count": count, "data": contacts, "has_more": count > len(contacts)}


@router.post(
    path="/search",
    summary="Search contacts",
    description="Search contacts with query string",
    tags=["Contacts"],
    status_code=200,
    response_model=ApiSearchResponse,
    response_description="The list of contacts",
)
def search_contacts(
    identity: Identity = Depends(identity_with_account),
    search: SearchQuery = BodyParams.SEARCH_CONTACTS,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    search_dict = search.dict()
    query = search_dict["query"]
    contacts = versify.contacts.search(account=identity.account.id, query=query)
    return {"count": len(contacts), "data": contacts}


@router.post(
    path="",
    summary="Create contact",
    description="Create a contact",
    tags=["Contacts"],
    status_code=201,
    response_model=Contact,
    response_description="The created contact",
)
def create_contact(
    identity: Identity = Depends(identity_with_account),
    contact_create: ContactCreate = BodyParams.CREATE_ASSET,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = contact_create.dict()
    body["account"] = identity.account.id
    create_result = versify.contacts.create(body)
    return create_result


@router.get(
    path="/{contact_id}",
    summary="Get contact",
    description="Get a contact",
    tags=["Contacts"],
    status_code=200,
    response_model=Contact,
    response_description="The contact",
)
def get_contact(
    identity: Identity = Depends(identity_with_account),
    contact_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    contact = versify.contacts.get(contact_id)
    if not contact:
        raise NotFoundException("Contact not found")
    if contact.account != identity.account.id:
        raise ForbiddenException()
    return contact


@router.put(
    path="/{contact_id}",
    summary="Update contact",
    description="Update an contact",
    tags=["Contacts"],
    status_code=200,
    response_model=Contact,
    response_description="The updated contact",
)
def update_contact(
    identity: Identity = Depends(identity_with_account),
    contact_id: str = PathParams.CONTACT_ID,
    contact_update: ContactUpdate = BodyParams.UPDATE_CONTACT,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    contact = versify.contacts.get(contact_id)
    if not contact:
        raise NotFoundException()
    if contact.account != identity.account.id:
        raise ForbiddenException()
    update_result = versify.contacts.update(contact_id, contact_update.dict())
    return update_result


@router.delete(
    path="/{contact_id}",
    summary="Delete contact",
    description="Delete an contact",
    tags=["Contacts"],
    status_code=200,
    response_model=ApiDeleteResponse,
    response_description="The deleted contact",
)
def delete_contact(
    identity: Identity = Depends(identity_with_account),
    contact_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    contact = versify.contacts.get(contact_id)
    if not contact:
        raise NotFoundException()
    if contact.account != identity.account.id:
        raise ForbiddenException()
    delete_result = versify.contacts.delete(contact_id)
    return delete_result
