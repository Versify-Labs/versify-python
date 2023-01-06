from app.api.deps import (
    current_active_account,
    current_active_user,
    current_user_account_role,
)
from app.api.exceptions import ForbiddenException, NotFoundException
from app.crud import versify
from app.models.account import Account
from app.models.contact import (
    ContactCreateRequest,
    ContactCreateResponse,
    ContactDeleteResponse,
    ContactGetResponse,
    ContactListRequest,
    ContactListResponse,
    ContactSearchRequest,
    ContactSearchResponse,
    ContactUpdateRequest,
    ContactUpdateResponse,
)
from app.models.enums import TeamMemberRole
from app.models.params import BodyParams, PathParams
from app.models.user import User
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/contacts", tags=["Contacts"])


@router.get(
    path="",
    summary="List contacts",
    description="List contacts with optional filters and pagination parameters",
    tags=["Contacts"],
    status_code=200,
    response_model=ContactListResponse,
    response_description="The list of contacts",
)
def list_contacts(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    contact_list_request: ContactListRequest = Depends(),
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.contacts.count(
        account=current_account.id,
        owner=contact_list_request.owner,
        status=contact_list_request.status,
    )
    contacts = versify.contacts.list(
        page_num=contact_list_request.page_num,
        page_size=contact_list_request.page_size,
        account=current_account.id,
        owner=contact_list_request.owner,
        status=contact_list_request.status,
    )
    return {"count": count, "data": contacts, "has_more": count > len(contacts)}


@router.post(
    path="/search",
    summary="Search contacts",
    description="Search contacts with query string",
    tags=["Contacts"],
    status_code=200,
    response_model=ContactSearchResponse,
    response_description="The list of contacts",
)
def search_contacts(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    contact_search_request: ContactSearchRequest = BodyParams.SEARCH_CONTACTS,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    contact_search_request_dict = contact_search_request.dict()
    query = contact_search_request_dict["query"]
    contacts = versify.contacts.search(account=current_account.id, query=query)
    return {"count": len(contacts), "data": contacts}


@router.post(
    path="",
    summary="Create contact",
    description="Create a contact",
    tags=["Contacts"],
    status_code=201,
    response_model=ContactCreateResponse,
    response_description="The created contact",
)
def create_contact(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    contact_create: ContactCreateRequest = BodyParams.CREATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = contact_create.dict()
    body["account"] = current_account.id
    create_result = versify.contacts.create(body)
    return create_result


@router.get(
    path="/{contact_id}",
    summary="Get contact",
    description="Get a contact",
    tags=["Contacts"],
    status_code=200,
    response_model=ContactGetResponse,
    response_description="The contact",
)
def get_contact(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    contact_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    contact = versify.contacts.get(contact_id)
    if not contact:
        raise NotFoundException()
    if contact.account != current_account.id:
        raise ForbiddenException()
    return contact


@router.put(
    path="/{contact_id}",
    summary="Update contact",
    description="Update an contact",
    tags=["Contacts"],
    status_code=200,
    response_model=ContactUpdateResponse,
    response_description="The updated contact",
)
def update_contact(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    contact_id: str = PathParams.CONTACT_ID,
    contact_update: ContactUpdateRequest = BodyParams.UPDATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    contact = versify.contacts.get(contact_id)
    if not contact:
        raise NotFoundException()
    if contact.account != current_account.id:
        raise ForbiddenException()
    body = contact_update.dict()
    update_result = versify.contacts.update(contact_id, body)
    return update_result


@router.delete(
    path="/{contact_id}",
    summary="Delete contact",
    description="Delete an contact",
    tags=["Contacts"],
    status_code=200,
    response_model=ContactDeleteResponse,
    response_description="The deleted contact",
)
def delete_contact(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    contact_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    contact = versify.contacts.get(contact_id)
    if not contact:
        raise NotFoundException()
    if contact.account != current_account.id:
        raise ForbiddenException()
    delete_result = versify.contacts.delete(contact_id)
    return delete_result
