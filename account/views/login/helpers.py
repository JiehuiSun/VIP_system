#!/usr/bin/env python
# mail: sunjiehui@chengantech.com
# author: huihui
# -*- coding: utf-8 -*-

import random
import hashlib
from flask import current_app


def algorithm_auth_login(user_id, random_str, timestamp):
    """
    算法登录验证
    :param user_id: integer
    :param random_str: string
    :param timestamp: integer
    :return: token: string
    """
    auth_login_key = current_app.config["APP_LOGIN_AUTH_KEY"]
    auth_code1 = hashlib.sha256(str("{0}{1}{2}".format(str(user_id), str(random_str), str(auth_login_key))).encode("utf8")).hexdigest()
    auth_code = hashlib.sha256(str("{0}{1}{2}".format(str(auth_code1), str(timestamp), str(auth_login_key))).encode("utf8")).hexdigest()

    ret_params = {
        "user_id": user_id,
        "random_str": random_str,
        "timestamp": timestamp,
        "auth_code": auth_code
    }

    return "{user_id}|{random_str}|{timestamp}|{auth_code}".format(**ret_params)


def make_random_str():
    ret = ''
    for i in range(10):
        num = random.randint(0,9)
        alfa = chr(random.randint(97,122))
        alfa2 = chr(random.randint(65,90))
        s = random.choice([str(num), alfa, alfa2])
        ret = ret+s
    return str(ret)

