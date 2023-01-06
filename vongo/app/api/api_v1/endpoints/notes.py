from app.api.deps import (
    current_active_account,
    current_active_user,
    current_user_account_role,
)
from app.crud import versify
from app.models.account import Account
from app.models.enums import TeamMemberRole
from app.api.exceptions import ForbiddenException, NotFoundException
from app.models.params import BodyParams, PathParams
from app.models.note import (
    NoteCreateRequest,
    NoteCreateResponse,
    NoteDeleteResponse,
    NoteGetResponse,
    NoteListRequest,
    NoteListResponse,
    NoteSearchRequest,
    NoteSearchResponse,
    NoteUpdateRequest,
    NoteUpdateResponse,
)
from app.models.user import User
from fastapi import APIRouter, Depends

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get(
    path="",
    summary="List notes",
    description="List notes with optional filters and pagination parameters",
    tags=["Notes"],
    status_code=200,
    response_model=NoteListResponse,
    response_description="The list of notes",
)
def list_notes(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    note_list_request: NoteListRequest = Depends(),
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    count = versify.notes.count(
        account=current_account.id,
    )
    notes = versify.notes.list(
        page_num=note_list_request.page_num,
        page_size=note_list_request.page_size,
        account=current_account.id,
    )
    return {"count": count, "data": notes, "has_more": count > len(notes)}


@router.post(
    path="/search",
    summary="Search notes",
    description="Search notes with query string",
    tags=["Notes"],
    status_code=200,
    response_model=NoteSearchResponse,
    response_description="The list of notes",
)
def search_notes(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    note_search_request: NoteSearchRequest = BodyParams.SEARCH_CONTACTS,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    note_search_request_dict = note_search_request.dict()
    query = note_search_request_dict["query"]
    notes = versify.notes.search(account=current_account.id, query=query)
    return {"count": len(notes), "data": notes}


@router.post(
    path="",
    summary="Create note",
    description="Create a note",
    tags=["Notes"],
    status_code=201,
    response_model=NoteCreateResponse,
    response_description="The created note",
)
def create_note(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    note_create: NoteCreateRequest = BodyParams.CREATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    body = note_create.dict()
    body["account"] = current_account.id
    create_result = versify.notes.create(body)
    return create_result


@router.get(
    path="/{note_id}",
    summary="Get note",
    description="Get a note",
    tags=["Notes"],
    status_code=200,
    response_model=NoteGetResponse,
    response_description="The note",
)
def get_note(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    note_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    note = versify.notes.get(note_id)
    if not note:
        raise NotFoundException()
    if note.account != current_account.id:
        raise ForbiddenException()
    return note


@router.put(
    path="/{note_id}",
    summary="Update note",
    description="Update an note",
    tags=["Notes"],
    status_code=200,
    response_model=NoteUpdateResponse,
    response_description="The updated note",
)
def update_note(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    note_id: str = PathParams.CONTACT_ID,
    note_update: NoteUpdateRequest = BodyParams.UPDATE_CONTACT,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    note = versify.notes.get(note_id)
    if not note:
        raise NotFoundException()
    if note.account != current_account.id:
        raise ForbiddenException()
    body = note_update.dict()
    update_result = versify.notes.update(note_id, body)
    return update_result


@router.delete(
    path="/{note_id}",
    summary="Delete note",
    description="Delete an note",
    tags=["Notes"],
    status_code=200,
    response_model=NoteDeleteResponse,
    response_description="The deleted note",
)
def delete_note(
    current_account: Account = Depends(current_active_account),
    current_user: User = Depends(current_active_user),
    current_user_account_role: TeamMemberRole = Depends(current_user_account_role),
    note_id: str = PathParams.CONTACT_ID,
):
    if current_user_account_role == TeamMemberRole.GUEST:
        raise ForbiddenException()
    note = versify.notes.get(note_id)
    if not note:
        raise NotFoundException()
    if note.account != current_account.id:
        raise ForbiddenException()
    delete_result = versify.notes.delete(note_id)
    return delete_result
