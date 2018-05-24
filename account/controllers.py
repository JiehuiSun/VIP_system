# 这里密码使用了明文存储，在实际使用中需要替换成加密后的密码来存储、比较
from account.models import User
from sqlalchemy import or_


def login(username, password):
    user = User.query.filter(or_(User.username==username, User.phone==username,
        User.email==username)).filter_by(is_deleted=False).one_or_none()
    if not user:
        return
    if user.password != password:
        return

    return user
