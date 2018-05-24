# 这里有一个点需要说明一下，return data
# 这个data最好采用dict的形式返回，这样在以后接口扩展时可以更好的支持
from flask import request
from api import Api
from api import errors
from . import controllers as account_ctl
from trace import session


class Login(Api):
    NEED_LOGIN = False

    def get(self):
        pass

    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not (username and password):
            raise errors.InvalidArgsError('请填写用户名和密码')
        user = account_ctl.login(username, password)
        token = session.set_session(user.id)
        data = {
            'token': token,
        }

        return data
