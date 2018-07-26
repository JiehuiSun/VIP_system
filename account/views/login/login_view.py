#!/usr/bin/env python
# mail: sunjiehuimail@foxmail.com
# author: huihui
# -*- coding: utf-8 -*-


import time
from flask import (request, jsonify)
from flask.views import MethodView
from framework.even_view import PostRPCView
from exc.even_exception import LogicError, RespOK
from account.models.UserModel import User
from api import Api
from .helpers import (algorithm_auth_login, make_random_str)


class Register(PostRPCView):
    """
    注册
    """
    decorators = []

    params_dict = {
        "username": "required",
        "password": "required"
    }

    def logic_func(self, params):
        if len(params["username"]) > 20 or len(params["password"]) > 20:
            ret = {
                'errcode': 12001,
                'errmsg': '注册失败，用户名或密码不符合规范',
            }
            raise LogicError(**ret)

        user_dict = User.register(params["username"], params["password"])
        print(user_dict)
        user_data = {
            "user_id": user_dict["data"].id
        }

        ret = {
            "errcode": 0,
            "data": user_data
        }
        return RespOK(**ret)


class Login(PostRPCView):
    """
    新登录
    """
    decorators = []

    params_dict = {
        "username": "required",
        "password": "required"
    }

    def logic_func(self, params):
        if not params["username"] or not params["password"]:
            ret = {
                'errcode': 12009,
                'errmsg': '登录失败，用户名或密码不能为空',
            }
            raise LogicError(**ret)
        params = {
            'username': str(params["username"]),
            'password': str(params["password"]),
        }
        ret = User.login(**params)
        if ret['errcode'] != 0:
            ret = {
                'errcode': 12008,
                'errmsg': '登录失败，用户名或密码错误',
            }
            raise LogicError(**ret)
        if ret["data"].active is False:
            ret = {
                'errcode': 12003,
                'errmsg': '您的账号已被禁用，请联系机构管理员'
            }
            raise LogicError(**ret)

        auth_code_params = {
            "user_id": ret["data"].id,
            "random_str": make_random_str(),
            "timestamp": int(time.time())
        }

        ret_code = algorithm_auth_login(**auth_code_params)

        ret_data = {
            'token': str(ret_code),
        }
        ret = {
            'errcode': 0,
            'errmsg': 'Login OK',
            'data': ret_data
        }
        return RespOK(**ret)


class LogoutView(MethodView):
    """
    退出登录
    """
    def post(self):
        ret = {
            'errcode': 0,
            'errmsg': 'Logout ok',
        }
        return jsonify(ret)

#
# instance.add_url_rule('/login', view_func=Login.as_view('login'), methods=['POST'])
# instance.add_url_rule('/logout', view_func=LogoutView.as_view('logout'), methods=['POST'])
