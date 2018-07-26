# 根据需求定义不同model
# username/email/phone没有做数据库级的唯一约束
# 因此需要在程序中进行限制, 为了解决用户删除后，再创建同样的用户问题

import bcrypt
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.exc import IntegrityError
from vip_system import db
from utils import time_utils


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean, default=True)
    is_deleted = db.Column(db.Boolean, default=False)
    dt_create = db.Column(db.DateTime, default=time_utils.now_dt)
    dt_update = db.Column(db.DateTime, default=time_utils.now_dt)

    @classmethod
    def register(cls, username, password,
                 is_active=True, ):
        try:
            passhash = bcrypt.hashpw(password.encode('utf-8'),
                                     bcrypt.gensalt())
            user = cls(username=username,
                       password=passhash,
                       active=is_active)
            db.session.add(user)
            db.session.commit()

            ret = {
                'errcode': 0,
                'errmsg': 'OK',
                'data': user,
            }
        except IntegrityError as e:
            db.session.rollback()
            ret = {
                'errcode': 1,
                'errmsg': '添加失败，该登录账号已存在',
            }
        except Exception as e:
            print(e)
            db.session.rollback()
            ret = {
                'errcode': 500,
                'errmsg': 'Database error occur',
            }
        return ret

    @classmethod
    def login(cls, username, password):
        try:
            user = cls.query.filter_by(username=username, is_deleted=False).one()
            if user.password.encode('utf-8') == bcrypt.hashpw(password.encode('utf-8'), user.password.encode('utf-8')):
                ret = {
                    'errcode': 0,
                    'errmsg': 'OK',
                    'data': user,
                }
            else:
                ret = {
                    'errcode': 1,
                    'errmsg': '密码输入错误,请重新输入',
                }
        except NoResultFound as e:
            db.session.rollback()
            ret = {
                'errcode': 2,
                'errmsg': '此用户不存在'
            }
        except MultipleResultsFound as e:
            db.session.rollback()
            ret = {
                'errcode': 3,
                'errmsg': 'duplicated user found, please check database'
            }
        except Exception as e:
            db.session.rollback()
            ret = {
                'errcode': 500,
                'errmsg': 'unknow database error occur',
            }
        return ret

    @classmethod
    def change_password(cls, username, password, new_password, force=False):
        passhash = bcrypt.hashpw(new_password.encode('utf-8'),
                                 bcrypt.gensalt())
        if force:
            try:
                user = cls.query.filter_by(username=username).one()
                user.passhash = passhash
                db.session.commit()
            except NoResultFound as e:
                ret = {
                    'errcode': 2,
                    'errmsg': 'user does not exist'
                }
            except MultipleResultsFound as e:
                ret = {
                    'errcode': 3,
                    'errmsg': 'duplicated user found, please check database'
                }
            except Exception as e:
                ret = {
                    'errcode': 500,
                    'errmsg': 'unknow database error occur',
                }
            return ret
        else:
            ret = cls.login(username, password)
            if ret['errcode'] == 0:
                user = ret['data']
                user.passhash = passhash
                db.session.commit()
            else:
                ret = {
                    'errmsg': '对不起，旧密码输入错误',
                    'errcode': 5,
                }
            return ret
