from werkzeug.security import safe_str_cmp
from models.user import User_Model


def authenticate(username, password):
    user = User_Model.get_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user


def identity(payload):
    user_id = payload["identity"]
    return User_Model.get_by_id(user_id)
