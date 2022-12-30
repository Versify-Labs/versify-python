from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/contacts",
    tags=["Contacts"]
)


@router.post(
    path="",
    summary="Create an contact",
    description="Create an contact",
    tags=["Contacts"],
    status_code=201,
    response_model=None,
    response_description="The created contact",
)
def create_contact(
    request: Request
):
    """
    Create Contact
    """
    return {"message": "Not implemented"}


@router.get(
    path="",
    summary="List contacts",
    description="List contacts with optional filters and pagination parameters",
    tags=["Contacts"],
    status_code=200,
    response_model=None,
    response_description="The list of contacts",
)
def list_contacts(
    request: Request
):
    """
    List Contacts
    """
    return {"message": "Not implemented"}


@router.get(
    path="/{contact_id}",
    summary="Get an contact",
    description="Get an contact",
    tags=["Contacts"],
    status_code=200,
    response_model=None,
    response_description="The contact",
)
def get_contact(
    request: Request
):
    """
    Get Contact
    """
    return {"message": "Not implemented"}


@router.put(
    path="/{contact_id}",
    summary="Update an contact",
    description="Update an contact",
    tags=["Contacts"],
    status_code=200,
    response_model=None,
    response_description="The updated contact",
)
def update_contact(
    request: Request
):
    """
    Update Contact
    """
    return {"message": "Not implemented"}


@router.delete(
    path="/{contact_id}",
    summary="Delete an contact",
    description="Delete an contact",
    tags=["Contacts"],
    status_code=200,
    response_model=None,
    response_description="The deleted contact",
)
def delete_contact(
    request: Request
):
    """
    Delete Contact
    """
    return {"message": "Not implemented"}


# from ..database import versify
# from ..dependencies import get_current_active_user
# from ..metadata import BodyParams
# from ..models import Contact, ContactCreate, User


# @router.post(
#     path="",
#     summary="Create a contact",
#     description="Create a contact",
#     status_code=status.HTTP_201_CREATED,
#     response_model=Contact,
#     response_description="The created contact",
# )
# async def create_account(
#     user: User = Depends(get_current_active_user),
#     # account_id: str = PathParams.ACCOUNT_ID,
#     contact: ContactCreate = BodyParams.CREATE_ACCOUNT,
# ):
#     body = contact.dict()
#     body["team"] = [{
#         "email": user.email,
#         "role": "admin",
#         "user": user.id
#     }]
#     created_contact = versify.create_contact(body)
#     return created_contact

# @router.get(
#     path="",
#     summary="List contacts",
#     description="List contacts with optional filters and pagination parameters",
#     status_code=status.HTTP_200_OK,
#     response_model=List[Contact],
#     response_description="The list of contacts",
# )
# async def list_contacts_for_account(
#     authorization: str = HeaderParams.AUTHORIZATION,
#     account_id: str = PathParams.ACCOUNT_ID,
#     active: Union[bool, None] = QueryParams.ACTIVE,
#     email:  Union[EmailStr, None] = QueryParams.EMAIL,
#     commons: ListQueryParams = Depends(),
# ):
#     if not authorization:
#         raise HTTPException(status_code=401, detail="Unauthorized")
#     if account_id not in [account['id'] for account in mock.accounts_db]:
#         raise HTTPException(status_code=404, detail="Contact not found")
#     filter = {
#         'account': account_id,
#         'active': active
#     }
#     if active is not None:
#         filter['active'] = active
#     if email:
#         filter['email'] = email
#     if commons.q:
#         filter['email'] = commons.q
#     return mock.contacts_db[commons.skip: commons.skip + commons.limit]

# @router.get(
#     path="/{contact_id}",
#     summary="Get a contact",
#     description="Get a contact for an account by ID",
#     status_code=status.HTTP_200_OK,
#     response_model=Contact,
#     response_description="The contact",
# )
# async def get_contact_for_account(
#     authorization: str = HeaderParams.AUTHORIZATION,
#     account_id: str = PathParams.ACCOUNT_ID,
#     contact_id: str = PathParams.CONTACT_ID,
# ):
#     if not authorization:
#         raise HTTPException(status_code=401, detail="Unauthorized")
#     if account_id not in [account['id'] for account in mock.accounts_db]:
#         raise HTTPException(status_code=404, detail="Contact not found")
#     return {"account": account_id, "contact": contact_id}

# @router.put(
#     path="/{contact_id}",
#     summary="Update a contact",
#     description="Update a contact for an account by ID",
#     status_code=status.HTTP_200_OK,
#     response_model=Contact,
#     response_description="The updated contact",
# )
# async def update_contact_for_account(
#     authorization: str = HeaderParams.AUTHORIZATION,
#     account_id: str = PathParams.ACCOUNT_ID,
#     contact_id: str = PathParams.CONTACT_ID,
#     contact_body: Contact = BodyParams.UPDATE_CONTACT
# ):
#     if not authorization:
#         raise HTTPException(status_code=401, detail="Unauthorized")
#     if account_id not in [account['id'] for account in mock.accounts_db]:
#         raise HTTPException(status_code=404, detail="Contact not found")
#     contact_body_encoded = jsonable_encoder(contact_body)
#     contact_output = versify.update_contact(contact_id, contact_body_encoded)
#     return contact_output
