#! /usr/bin/env python3.6
# -*- coding: utf-8 -*-
# Author: Lee <lee@chengantech.com>
# Date: 2018-02-13


import re
import types
from flask import current_app, request, jsonify
from flask.views import View
from flask_login import current_user
from werkzeug.exceptions import BadRequest
from api import Api
from exc import RespOK, LogicError, SysError


class PostRPCView(View):
    '''
    PostRPCView

    use post method only
    action like a rpc method
    '''

    methods = ['POST', ]
    params_dict = dict()

    def dispatch_request(self):
        self.request = request
        self.current_app = current_app
        self.current_user = current_user

        try:
            data = request.get_json()
            params = self.__preprocess_req(data)
            ret = self.logic_func(params)
            raise ret
        except BadRequest as e:
            current_app.logger.exception(e)
            ret = {
                'errcode': 12001,
                'errmsg': str(e),
            }
        except LogicError as e:
            current_app.logger.exception(e)
            ret = {
                'errcode': e.errcode,
                'errmsg': e.errmsg,
            }
        except SysError as e:
            current_app.logger.exception(e)
            ret = {
                'errcode': e.errcode,
                'errmsg': e.errmsg,
            }
        except RespOK as e:
            # 如果是OK，不记录Exception，因为是正常的业务返回
            # current_app.logger.exception(e)
            ret = {
                'errcode': e.errcode,
                'errmsg': e.errmsg,
                'data': e.data,
            }
        except Exception as e:
            current_app.logger.exception(e)
            ret = {
                'errcode': 50000,
                'errmsg': str(e),
            }
        return jsonify(ret)

    def logic_func(self, params):
        '''
        this real logic

        方法的参数必须明确, 如下所示
        logic_func(x, y, z)
        '''
        raise NotImplementedError(
            'logic_func is not implemented')

    def __preprocess_req(self, data):
        '''
        __preprocess_req 检验参数方法

        所有logic_func 的方法参数必须
        在这个方法被妥善检查
        '''
        data_keys = set(data.keys())
        max_keys = set(self.params_dict.keys())
        # mini keys 判断
        min_keys = set()
        for k in max_keys:
            check_method = self.params_dict[k]
            if isinstance(check_method, types.FunctionType):
                continue
            params_dict_list = self.params_dict[k].split(' ')
            if 'optional' not in params_dict_list:
                min_keys.add(k)
        overflow_keys = data_keys - max_keys
        lack_keys = min_keys - data_keys

        # 验证后端需要的key 传递情况
        flag_keys_not_match = False
        errmsg_keys_not_match = ''
        if overflow_keys:
            flag_keys_not_match = True
            errmsg_keys_not_match += '请求参数中, 多余的key包括: '
            errmsg_keys_not_match += ', '.join([str(k) for k in overflow_keys])
        if lack_keys:
            flag_keys_not_match = True
            errmsg_keys_not_match += '请求参数中, 缺少的key包括: '
            errmsg_keys_not_match += ', '.join([str(k) for k in lack_keys])
        if flag_keys_not_match:
            raise LogicError(errcode=12001, errmsg=errmsg_keys_not_match)

        # 根据params_dict 逐条验证参数.
        params = dict()
        errmsg_keys_valid = []
        for k, v in data.items():
            flag = False
            msg = ''
            check_method = self.params_dict[k]
            # 执行用户自定义验证方法
            if isinstance(check_method, types.FunctionType):
                flag, msg = check_method(v, k)
            elif isinstance(check_method, str):
                check_method_list = check_method.split(' ')
                for item_method in check_method_list:
                    flag, msg = getattr(self, '_valid_'+item_method)(v, k)
                    if not flag:
                        break
                # 执行默认方法
            if not flag:
                errmsg_keys_valid.append(msg)
                continue
            params[k] = v
        if errmsg_keys_valid:
            errmsg = ' '.join(errmsg_keys_valid)
            raise LogicError(errcode=12001, errmsg=errmsg)
        return params

    def _valid_tel(self, i, key_name=None):
        if re.match(r"\d{11}$", str(i)) != None:
            return True, 'OK'
        return False ,'请填入正确电话号码'

    def _valid_str(self, i, key_name=None):
        if isinstance(i, str):
            return True, 'OK'
        return False, key_name

    def _valid_list(self, i, key_name=None):
        if isinstance(i, list):
            return True, 'OK'
        return False, '请输入列表'

    def _valid_cash(self, i, key_name=None):
        # TODO 关于金额方面的验证方法
        # TODO 关于验证信息的展示
        amount = i.get('amount')
        currency_id = i.get('currency_id')
        num = i.get('num')
        unit_id = i.get('unit_id')
        if amount is not None and currency_id is not None:
            try:
                amount = float(amount)
            except ValueError as e:
                return False, '金额输入错误, 请输入数字'
            try:
                currency_id = int(currency_id)
            except ValueError as e:
                return False, '币种选择错误'
            return True, 'OK'
        if num is not None and unit_id is not None:
            try:
                num= float(num)
            except ValueError as e:
                return False, '金额输入错误, 请输入数字'
            try:
                unit_id = int(unit_id)
            except ValueError as e:
                return False, '币种选择错误'
            return True, 'OK'
        return False, '{0} 无法正确解析, 请联系技术人员, 或检查参数格式'.format(key_name)

    def _valid_required(self, i, key_name=None):
        '''
        该参数必须有值, 并且判断不能为 False
        '''
        if i:
            return True, key_name
        return False, key_name

    def _valid_optional(self, i, key_name=None):
        '''
        该参数可以不存在
        '''
        return True, 'OK'

    def _valid_pass(self, i, key_name=None):
        '''
        该参数必须存在, 但不需要验证
        '''
        return True, 'OK'

    def _valid_list(self, i, key_name=None):
        '''
        参数必须为list类型
        '''
        if isinstance(i, list):
            return True, 'OK'
        return False, '{0} 必须为list(array)类型, 谢谢配合!'.format(key_name)

    def _valid_int(self, i, key_name=None):
        '''
        参数必须为int类型
        '''
        if isinstance(i, int):
            return True, 'OK'
        return False, '{0} 必须为int(整型)类型, 谢谢配合!'.format(key_name)
