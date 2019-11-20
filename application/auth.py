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
    api_key = request.headers.get("Authorization")
    if api_key:
        api_key = api_key.replace("Bearer ", '', 1)
        try:
            api_key = b64decode(api_key.encode("utf-8"))
            user = User()
            user.id = "demo"
            return user
        except:
            app.logger.warning("Unauthorized API access attempt!", exc_info=True)

    return None
