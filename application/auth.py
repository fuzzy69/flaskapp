from flask_login import UserMixin
from werkzeug.security import check_password_hash

from application.base import login_manager


USERS = {
    "demo": "pbkdf2:sha256:150000$Lgdmfr9X$bbb8229c62e63824d6f53de5930b5add6bfdffcbda745d653aa26c044c69e7d9",
}


class User(UserMixin):
    """"""
    pass


# @login_manager.user_loader
# def load_user(user_id: str) -> User:
#     """"""
#     return User.get_id(user_id)


@login_manager.user_loader
def load_user(email: str):
    """"""
    if email not in USERS:
        return

    user = User()
    user.id = email

    return user


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
