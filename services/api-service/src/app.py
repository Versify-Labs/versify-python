from flask import Flask, request
from flask_pydantic import validate
from src.responses import (
    make_bad_request_error_response,
    make_forbidden_error_response,
    make_get_response,
    make_internal_server_error_response,
    make_not_found_error_response,
    make_not_implemented_error_response,
    make_unauthorized_error_response,
)
from src.utils.data_classes import Identity

from versify import Versify
from versify.models.account import (
    AccountAdminResponse,
    AccountCreateRequest,
    AccountDeletedResponse,
    AccountListResponse,
    AccountMemberResponse,
    AccountPublicResponse,
    AccountUpdateRequest,
)
from versify.models.contact import (
    ContactCreateRequest,
    ContactDeletedResponse,
    ContactListFilter,
    ContactListQuery,
    ContactListResponse,
    ContactResponse,
    ContactUpdateRequest,
)

app = Flask(__name__)
versify = Versify()

API_VERSION = "v2"


@app.errorhandler(400)
def bad_request(error):
    return make_bad_request_error_response(error.description)


@app.errorhandler(401)
def unauthorized(error):
    return make_unauthorized_error_response(error.description)


@app.errorhandler(403)
def forbidden(error):
    return make_forbidden_error_response(error.description)


@app.errorhandler(404)
def not_found(error):
    return make_not_found_error_response(error.description)


@app.errorhandler(500)
def internal_server_error(error):
    return make_internal_server_error_response(error.description)


@app.errorhandler(501)
def not_implemented(error):
    return make_not_implemented_error_response(error.description)


@app.before_request
def before_request():
    print("before_request")

    # Validate the request headers
    auth = request.headers.get("Authorization", "")
    auth_type, auth_token = auth.split(" ", 1) if " " in auth else (None, None)
    setattr(request, "identity", Identity(auth_type, auth_token))
    # TODO: Validate the request body
    # TODO: Validate the account subscription status based on the identity
    # TODO: Save the request to logs for debugging


@app.after_request
def after_request(response):
    print("after_request")
    # TODO: Expand response if needed
    # TODO: Filter response based on identity
    # TODO: Save response to logs for debugging
    return response


@app.route(f"/{API_VERSION}/oauth/authorize", methods=["GET", "POST"])
def authorize():
    # TODO: Validate Stytch token
    # TODO: Get the user info from the Stytch token
    # TODO: Generate a code
    # TODO: Return the code
    # data = {
    #     'code': 'Not implemented',
    #     'state': 'Not implemented'
    # }
    return make_not_implemented_error_response()


@app.route(f"/{API_VERSION}/oauth/access_token", methods=["POST"])
def access_token():
    # TODO: Validate the code
    # TODO: Get the user info from the code
    # TODO: Generate an access token
    # TODO: Return the access token
    # data = {
    #     'access_token': 'Not implemented',
    #     'expires_in': 3600,
    #     'token_type': 'Bearer',
    # }
    return make_not_implemented_error_response()


@app.route(f"/{API_VERSION}/oauth/user_info", methods=["GET"])
def user_info():
    identity = getattr(request, "identity")
    if not identity.is_active:
        return make_unauthorized_error_response()
    data = {
        "user": identity.user,
        "roles": identity.roles,
    }
    return make_get_response(data)


@app.route(f"/{API_VERSION}/accounts", methods=["POST"])
@validate(body=AccountCreateRequest, on_success_status=201)
def create_account():

    # Parse request
    body = request.json or {}
    identity = getattr(request, "identity")

    # Validate access
    if not identity.is_active:
        return make_unauthorized_error_response()

    # Process request
    body["email"] = identity.user["email"]
    account = versify.account_service.create(body)

    # Return response
    return AccountAdminResponse(**account)


@app.route(f"/{API_VERSION}/accounts", methods=["GET"])
@validate(on_success_status=200)
def list_accounts():

    # Parse request
    identity = getattr(request, "identity")

    # Validate access
    if not identity.is_active:
        return make_unauthorized_error_response()

    # Process request
    accounts = []
    for account in identity.user.get("accounts", []):
        account_id = account["id"]
        if identity.has_account_role(account_id, "admin"):
            account = AccountAdminResponse(**account)
        elif identity.has_account_role(account_id, "member"):
            account = AccountMemberResponse(**account)
        else:
            account = AccountPublicResponse(**account)
        accounts.append(account)

    # Return response
    return AccountListResponse(data=accounts, count=len(accounts))


@app.route(f"/{API_VERSION}/accounts/<account_id>", methods=["GET"])
@validate(on_success_status=200)
def get_account(account_id):

    # Parse request
    identity = getattr(request, "identity")

    # Process request
    account = versify.account_service.get(account_id)
    if not account:
        return make_not_found_error_response("Account not found.")

    # Return response based on identity
    if identity.has_account_role(account_id, "admin"):
        return AccountAdminResponse(**account)
    elif identity.has_account_role(account_id, "member"):
        return AccountMemberResponse(**account)
    else:
        return AccountPublicResponse(**account)


@app.route(f"/{API_VERSION}/accounts/<account_id>", methods=["PUT"])
@validate(body=AccountUpdateRequest, on_success_status=200)
def update_account(account_id):

    # Parse request
    body = request.json or {}
    identity = getattr(request, "identity")

    # Validate access
    has_access, message = identity.has_access(account_id, ["admin", "member"])
    if not has_access:
        return make_unauthorized_error_response(message)

    # Process request
    account = versify.account_service.update(account_id, body)

    # Return response based on identity
    if identity.has_account_role(account_id, "admin"):
        return AccountAdminResponse(**account)
    elif identity.has_account_role(account_id, "member"):
        return AccountMemberResponse(**account)
    else:
        return AccountPublicResponse(**account)


@app.route(f"/{API_VERSION}/accounts/<account_id>", methods=["DELETE"])
@validate(on_success_status=200)
def delete_account(account_id):

    # Parse request
    identity = getattr(request, "identity")

    # Validate access
    has_access, message = identity.has_access(account_id, ["admin"])
    if not has_access:
        return make_unauthorized_error_response(message)

    # Process request
    deleted = versify.account_service.delete(account_id)
    if not deleted:
        return make_not_found_error_response("Account not found.")

    # Return response
    return AccountDeletedResponse(id=account_id)


@app.route(f"/{API_VERSION}/accounts/<account_id>/contacts", methods=["POST"])
@validate(body=ContactCreateRequest, on_success_status=201)
def create_contact(account_id: str):

    # Parse request
    body = request.body_params.dict()  # type: ignore
    identity = getattr(request, "identity")

    # Validate access
    has_access, message = identity.has_access(account_id)
    if not has_access:
        return make_unauthorized_error_response(message)

    # Process request
    body["account"] = account_id
    contact = versify.contact_service.create(body)

    # Return response
    return ContactResponse(**contact)


@app.route(f"/{API_VERSION}/accounts/<account_id>/contacts", methods=["GET"])
@validate(query=ContactListQuery, on_success_status=200)
def list_contacts(account_id):

    # Parse request
    identity = getattr(request, "identity")

    # Validate access
    if not identity.has_account_access(account_id, ["admin", "member"]):
        return make_unauthorized_error_response()

    # Process request
    # filter = ContactListFilter(
    #     account=account_id,
    #     **request.query_params.dict()
    # )
    filter = {"account": account_id}
    limit = request.query_params.limit
    skip = request.query_params.skip

    count = versify.contact_service.count(filter)
    contacts = versify.contact_service.list(filter, limit, skip)
    if request.query_params.expand:
        expand_list = request.query_params.expand.split(",")
        contacts = versify.contact_service.expand(contacts, expand_list)

    # Return response
    return ContactListResponse(data=contacts, count=count)


@app.route(
    f"/{API_VERSION}/accounts/<account_id>/contacts/<contact_id>", methods=["GET"]
)
@validate(on_success_status=200)
def get_contact(account_id, contact_id):

    # Parse request
    identity = getattr(request, "identity")

    # Validate access
    if not identity.has_account_access(account_id, ["admin", "member"]):
        return make_unauthorized_error_response()

    # Process request
    contact = versify.contact_service.get(contact_id)
    if not contact:
        return make_not_found_error_response("Contact not found.")

    # Return response
    return ContactResponse(**contact) if contact else make_not_found_error_response()


@app.route(
    f"/{API_VERSION}/accounts/<account_id>/contacts/<contact_id>", methods=["PUT"]
)
@validate(body=ContactUpdateRequest, on_success_status=200)
def update_contact(account_id, contact_id):

    # Parse request
    body = request.body_params.dict()  # type: ignore
    identity = getattr(request, "identity")

    # Validate access
    if not identity.has_account_access(account_id, ["admin", "member"]):
        return make_unauthorized_error_response()

    # Process request
    body["account"] = account_id
    contact = versify.contact_service.update(contact_id, body)

    # Return response
    return ContactResponse(**contact)


@app.route(
    f"/{API_VERSION}/accounts/<account_id>/contacts/<contact_id>", methods=["DELETE"]
)
@validate(on_success_status=200)
def delete_contact(account_id, contact_id):

    # Parse request
    identity = getattr(request, "identity")

    # Validate access
    if not identity.has_account_access(account_id, ["admin", "member"]):
        return make_unauthorized_error_response()

    # Process request
    deleted = versify.contact_service.delete(contact_id)
    if not deleted:
        return make_not_found_error_response("Contact not found.")

    # Return response
    return ContactDeletedResponse(id=contact_id)
