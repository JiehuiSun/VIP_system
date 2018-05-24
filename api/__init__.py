# 这里写一个基础接口类，以后所以接口都需要继承此类
# __call__方法是为了使用此类可以直接像方法一样调用
# 异常处理时，先捕捉BaseError，我们将BaseError当成
# 正常的业务异常；之后捕捉Exception，就是系统异常，
# 需要进行日志记录等操作
from flask import request
from flask import jsonify
from flask import current_app
from easy_flask import errors
from easy_flask import session


class Api(object):
    NEED_LOGIN = True

    def __init__(self):
        self.__name__ = self.__class__.__name__

    def _get_token(self):
        token = request.headers.get('HTTP-X-TOKEN')
        if not token:
            raise errors.NoTokenError
        return token

    def _identification(self):
        if self.NEED_LOGIN:
            self.token = self._get_token()
            self.user_id = session.get_session(self.token)
            if not self.user_id:
                raise errors.LoginExpiredError

    def _pre_handle(self):
        """
            调用具体业务方法之前，如果需要一些权限认证或者其它操作在这里实现
        """
        self._identification()

    def _after_handle(self):
        """
            调用具体业务方法后，如果需要一些结果处理等在这里实现
        """
        pass

    def __call__(self, *args, **kwargs):
        data = ''
        errno = 0
        errmsg = ''
        try:
            method = getattr(self, request.method.lower(), None)
            if not method:
                raise errors.MethodError
            self._pre_handle()
            data = method(*args, **kwargs)
            self._after_handle()
        except errors.BaseError as e:
            errno = e.errno
            errmsg = e.errmsg
        except Exception as e:
            current_app.logger.exception(e)
            errno = errors.BaseError.errno
            errmsg = errors.BaseError.errmsg
        result = {
            'errno': errno,
            'errmsg': errmsg,
            'data': data,
        }

        return jsonify(result)
