# 这里有一个点需要说明一下，return data
# 这个data最好采用dict的形式返回，这样在以后接口扩展时可以更好的支持
from flask import request
from api import Api
from api import errors
from account import controllers as account_ctl
from vip_system import session


class Login(Api):
    NEED_LOGIN = False

    def get(self):
        pass

    def post(self):
        data = request.get_json()
        username = str(data.get('username'))
        password = str(data.get('password'))
        if not (username and password):
            raise errors.InvalidArgsError('请填写用户名和密码')
        user = account_ctl.login(username, password)
        token = session.set_session(user.id)
        data = {
            'token': token,
        }

        return data


#  class LoginPermanent(Api):
    #  """
    #  新登录
    #  """
    #  decorators = []

    #  params_dict = {
        #  "username": "required",
        #  "password": "required"
    #  }

    #  def logic_func(self, params):
        #  if not params["username"] or not params["password"]:
            #  ret = {
                #  'errcode': 12009,
                #  'errmsg': '登录失败，用户名或密码不能为空',
            #  }
            #  raise LogicError(**ret)
        #  params = {
            #  'username': str(params["username"]),
            #  'password': str(params["password"]),
        #  }
        #  ret = CompanyUserModel.login(**params)
        #  if ret['errcode'] != 0:
            #  ret = {
                #  'errcode': 12008,
                #  'errmsg': '登录失败，用户名或密码错误',
            #  }
            #  raise LogicError(**ret)
        #  if ret["data"].is_active() is False:
            #  ret = {
                #  'errcode': 12003,
                #  'errmsg': '您的账号已被禁用，请联系机构管理员'
            #  }
            #  raise LogicError(**ret)

        #  auth_code_params = {
            #  "user_id": ret["data"].id,
            #  "random_str": make_random_str(),
            #  "timestamp": int(time.time())
        #  }

        #  ret_code = algorithm_auth_login(**auth_code_params)

        #  notify_params = {
            #  "user_id": auth_code_params["user_id"],
            #  "status": "unread"
        #  }
        #  unread_notify_count = len(list_notify_by_receiver(**notify_params))

        #  user_detail = CompanyUserDetailModel.query.filter_by(user_id=ret["data"].id).one()

        #  phone_bind_count = count_company_user_bind_phone(company_id=user_detail.company_id, user_id=ret["data"].id)

        #  try:
            #  user_bind_phone_obj = CompanyUserBindPhoneModel.query.filter_by(user_id=user_detail.user_id,
                                                                            #  is_deleted=False).all()[0]
            #  user_phone = user_bind_phone_obj.phone
        #  except Exception as e:
            #  user_phone = ""

        #  headers_params = request.headers
        #  device_typ = headers_params.get("device_typ", "")
        #  channel_id = headers_params.get("channel_id", "")
        #  app_version = headers_params.get("version", "")

        #  device_params = {
            #  "company_id": user_detail.company_id,
            #  "user_id": user_detail.user_id,
            #  "version": app_version,
            #  "device_typ": device_typ,
            #  "channel_id": channel_id
        #  }
        #  create_user_device_info(**device_params)

        #  user_dict = {
            #  "user_id": ret["data"].id,
            #  "chinese_name": user_detail.chinese_name
            #  }

        #  wechat_bind_count = CompanyUserBindWechatModel.query.filter_by(user_id=user_detail.user_id,
                                                                #  company_id=user_detail.company_id,
                                                                #  is_deleted=False).count()


        #  ret_data = {
            #  'token': str(ret_code),
            #  "notify_count": unread_notify_count,
            #  "user_data": user_dict,
            #  "phone_bind_count": phone_bind_count,
            #  "wechat_bind_count": wechat_bind_count,
            #  "user_phone": str(user_phone)
        #  }
        #  ret = {
            #  'errcode': 0,
            #  'errmsg': 'Login OK',
            #  'data': ret_data
        #  }
        #  return RespOK(**ret)
