from flask import request
from sqlalchemy.sql.expression import bindparam, text

from skeleton import cache, db
from .models.user_info import UserInfo

@cache.memoize()
def get_user_id(email = None):
    """ Helper function that returns the user_id for a given email address """
    if email is not None:
        result = db.session.execute(
            text("SELECT aaa.user_id_get(:email)",
                 bindparams=[bindparam('email', email)]))
        return result.first()[0]
    return None


@cache.memoize()
def get_user_timezone(user_id = None, email = None):
    """ Helper function that returns the user's timezone """
    if email is not None:
        user_id = get_user_id(email)

    if user_id is not None:
        return UserInfo.query.filter_by(user_id=user_id).first().timezone.name

    return None
