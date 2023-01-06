from flask import jsonify, make_response, url_for
from pydantic import BaseModel


def make_get_response(data):
    if isinstance(data, BaseModel):
        data = data.dict()
    return make_response(jsonify(data), 200)


def make_list_response(data, endpoint, has_more=False, count=None):
    if isinstance(data, BaseModel):
        data = data.dict()
    data = {
        "object": "list",
        "url": url_for(endpoint),
        "has_more": has_more,
        "data": data,
        "count": count,
    }
    return make_response(jsonify(data), 200)


def make_update_response(data):
    if isinstance(data, BaseModel):
        data = data.dict()
    return make_response(jsonify(data), 200)


def make_delete_response(id, object):
    data = {"id": id, "object": object, "deleted": True}
    return make_response(jsonify(data), 200)


def make_create_response(data):
    if isinstance(data, BaseModel):
        data = data.dict()
    return make_response(jsonify(data), 201)


def make_bad_request_error_response(message="Bad request"):
    return make_response(jsonify({"message": message}), 400)


def make_unauthorized_error_response(message="Unauthorized"):
    return make_response(jsonify({"message": message}), 401)


def make_forbidden_error_response(message="Forbidden"):
    return make_response(jsonify({"message": message}), 403)


def make_not_found_error_response(message="Not found"):
    return make_response(jsonify({"message": message}), 404)


def make_internal_server_error_response(message="Internal server error"):
    return make_response(jsonify({"message": message}), 500)


def make_not_implemented_error_response(message="Not implemented"):
    return make_response(jsonify({"message": message}), 501)
