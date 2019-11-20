# -*- coding: UTF-8 -*-

from base64 import b64decode
from typing import Optional

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash

from application.base import db, login_manager
from application.models import UsersTable


app = current_app


class User(UserMixin):
    """Represents logged in user"""
    pass


@login_manager.user_loader
def load_user(username: str) -> Optional[User]:
    """Checks user session. Return User instance if valid user otherwise None"""
    r = db.session.query(UsersTable).filter(UsersTable.username == username).first()
    if r is None:
        return

    user = User()
    user.id = username

    return user


@login_manager.request_loader
def load_user_from_request(request):
    """Checks if request contains valid API key header"""
    auth_header = request.headers.get("Authorization")
    if any((auth_header is None, ':' not in auth_header, "Bearer " not in auth_header)):
        app.logger.warning("Invalid authorization header!")
        return None
    username, api_key = auth_header.replace("Bearer ", '', 1).split(':', 1)
    r = db.session.query(UsersTable).filter(UsersTable.username == username).first()
    if r is not None:
        try:
            decoded_api_key = b64decode(api_key.encode("utf-8"))
            if not check_password_hash(r.api_key, decoded_api_key):
                app.logger.warning("Invalid API key '{}'!".format(api_key))
                return None
            user = User()
            user.id = r.username
            return user
        except:
            app.logger.warning("Failed to decode API key '{}'!".format(api_key), exc_info=True)

    return None
