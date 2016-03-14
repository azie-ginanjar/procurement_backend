from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)

from ..utils import (
    make_response_body,
    render_json,
    validate_schema,
    id_generator,
)

from flask import Blueprint
from flask import current_app
from flask import request
import hashlib

from ..database import ApplicationKey, ProcurementUsers, AuthenticationToken, db
from .schema import LoginSchema, RegisterSchema


user_api = Blueprint("user_api", __name__)

@user_api.route("/login", methods=["POST"])
@render_json
def handle_login(): 
    body = make_response_body()

    app_key = ApplicationKey.find_by_app_key(request.headers.get('app_key'))

    if not app_key:
        body["error"] = {"message": "Application Key not found"}
        return body, 404

    validation = validate_schema(request.form, LoginSchema())

    if validation.errors:
        body["error"] = {"message": validation.errors}
        return body, 400


    users = ProcurementUsers.find_by_username_password(validation.args["username"], validation.args["password"])

    if not users:
        body["error"] = {"message": "Users not found"}
        return body, 404

    random_string = id_generator(size=40)

    token = AuthenticationToken()
    token.access_token = random_string
    token.user_id = users.id
    token.status = 1
    token.app_key = request.headers.get('app_key')
    db.session.add(token)
    db.session.commit()

    result = [{
        "access_token": random_string,
    }]

    body["objects"] = result

    return body, 200

@user_api.route("/logout", methods=["POST"])
@render_json
def handle_logout(): 
    body = make_response_body()
    app_key = ApplicationKey.find_by_app_key(request.headers.get('app_key'))

    if not app_key:
        body["error"] = {"message": "Application Key not found"}
        return body, 404

    auth_token = AuthenticationToken.find_by_access_token(request.headers.get('access_token'))
    if not auth_token:
        body["error"] = {"message": "Access token not found"}
        return body, 404

    for token in auth_token:
        token.status = 1
        db.session.add(token)
    db.session.commit()

    body["objects"] = [{
        "message": "logout success",
    }]

    return body, 200

@user_api.route("/register", methods=["POST"])
@render_json
def add_register():
    """ Register User
    """
    body = make_response_body()
    validation = validate_schema(request.form, RegisterSchema())
    if validation.errors:
        body["error"] = {"message": validation.errors}
        return body, 400

    users = ProcurementUsers()
    users.username = validation.args["username"]
    users.password = validation.args["password"]
    db.session.add(users)
    db.session.commit()

    body["objects"] = [{
        "username": users.username,
        "password": users.password,
    }]
    return body, 200

@user_api.route("/myhash", methods=["GET"])
def handle_myhash(): 
    myhash = hashlib.sha1(b"faruq anak soleh").hexdigest()
    return myhash, 200