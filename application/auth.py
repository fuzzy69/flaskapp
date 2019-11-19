from base64 import b64decode, b16encode

from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash

from application.base import login_manager


app = current_app

USERS = {
    "demo": (
        "pbkdf2:sha256:150000$Lgdmfr9X$bbb8229c62e63824d6f53de5930b5add6bfdffcbda745d653aa26c044c69e7d9",  # password
        "ZGVtb3Rva2Vu"  # access token
    ),
}


class User(UserMixin):
    """"""
    pass


# @login_manager.user_loader
# def load_user(user_id: str) -> User:
#     """"""
#     return User.get_id(user_id)


@login_manager.user_loader
def load_user(username: str):
    """"""
    if username not in USERS:
        return

    user = User()
    user.id = username

    return user


# @login_manager.header_loader
# def load_user_from_header(header_val):
#     header_val = header_val.replace('Basic ', '', 1)
#     try:
#         header_val = base64.b64decode(header_val)
#     except TypeError:
#         pass
#     return User.query.filter_by(api_key=header_val).first()


@login_manager.request_loader
def load_user_from_request(request):
    """"""
    api_key = request.headers.get("Authorization")
    if api_key:
        api_key = api_key.replace("Bearer ", '', 1)
        try:
            api_key = b64decode(api_key.encode("utf-8"))
            user = User()
            user.id = "demo"
            return user
        except:
            app.logger.warning("Un-authorized API access attempt!", exc_info=True)

    return None


class Users:
    """"""
    def __init__(self, username: str, password: str):
        """"""
        self._username = username
        self.password = password
        self.set_password(password)

    # def set_password(self, password):
    #     self.pw_hash = generate_password_hash(password)

    def check_password(self, password_hash):
#        if not password_hash:
#            return check_password_hash(self.pw_hash, password)
        return check_password_hash(password_hash, self.password)
