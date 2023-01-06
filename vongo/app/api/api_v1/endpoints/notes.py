from ...deps import identity_with_account
from app.crud import versify
from ...models import (
    ApiDeleteResponse,
    ApiListResponse,
    ApiSearchResponse,
    BodyParams,
    Identity,
    PathParams,
    QueryParams,
    SearchQuery,
)
from app.models.note import Note, NoteCreate, NoteUpdate

from app.models.enums import TeamMemberRole
from ...exceptions import ForbiddenException, NotFoundException
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get(
    path="",
    summary="List notes",
    description="List notes with optional filters and pagination parameters",
    tags=["Notes"],
    status_code=200,
    response_model=ApiListResponse,
    response_description="The list of notes",
)
def list_notes(
    identity: Identity = Depends(identity_with_account),
    page_num: int = QueryParams.PAGE_NUM,
    page_size: int = QueryParams.PAGE_SIZE,
    collection: str = QueryParams.COLLECTION_ID,
    status: str = QueryParams.COLLECTION_STATUS,
):
    if identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.notes.count(
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    notes = versify.notes.list(
        page_num=page_num,
        page_size=page_size,
        account=identity.account.id,  # type: ignore
        collection=collection,
        status=status,
    )
    return {"count": count, "data": notes, "has_more": count > len(notes)}


@router.post(
    path="/search",
    summary="Search notes",
    description="Search notes with query string",
    tags=["Notes"],
    status_code=200,
    response_model=ApiSearchResponse,
    response_description="The list of notes",
)
def search_notes(
    identity: Identity = Depends(identity_with_account),
    search: SearchQuery = BodyParams.SEARCH_CONTACTS,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    search_dict = search.dict()
    query = search_dict["query"]
    notes = versify.notes.search(account=identity.account.id, query=query)
    return {"count": len(notes), "data": notes}


@router.post(
    path="",
    summary="Create note",
    description="Create a note",
    tags=["Notes"],
    status_code=201,
    response_model=Note,
    response_description="The created note",
)
def create_note(
    identity: Identity = Depends(identity_with_account),
    note_create: NoteCreate = BodyParams.CREATE_ASSET,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = note_create.dict()
    body["account"] = identity.account.id
    create_result = versify.notes.create(body)
    return create_result


@router.get(
    path="/{note_id}",
    summary="Get note",
    description="Get a note",
    tags=["Notes"],
    status_code=200,
    response_model=Note,
    response_description="The note",
)
def get_note(
    identity: Identity = Depends(identity_with_account),
    note_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    note = versify.notes.get(note_id)
    if not note:
        raise NotFoundException("Note not found")
    if note.account != identity.account.id:
        raise ForbiddenException()
    return note


@router.put(
    path="/{note_id}",
    summary="Update note",
    description="Update an note",
    tags=["Notes"],
    status_code=200,
    response_model=Note,
    response_description="The updated note",
)
def update_note(
    identity: Identity = Depends(identity_with_account),
    note_id: str = PathParams.CONTACT_ID,
    note_update: NoteUpdate = BodyParams.UPDATE_CONTACT,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    note = versify.notes.get(note_id)
    if not note:
        raise NotFoundException()
    if note.account != identity.account.id:
        raise ForbiddenException()
    update_result = versify.notes.update(note_id, note_update.dict())
    return update_result


@router.delete(
    path="/{note_id}",
    summary="Delete note",
    description="Delete an note",
    tags=["Notes"],
    status_code=200,
    response_model=ApiDeleteResponse,
    response_description="The deleted note",
)
def delete_note(
    identity: Identity = Depends(identity_with_account),
    note_id: str = PathParams.CONTACT_ID,
):
    if not identity.account or identity.account_user_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    note = versify.notes.get(note_id)
    if not note:
        raise NotFoundException()
    if note.account != identity.account.id:
        raise ForbiddenException()
    delete_result = versify.notes.delete(note_id)
    return delete_result
