# 定义BaseError，其它所有错误类都继承BaseError
# 设定对应的errno和errmsg
# 正常使用时，raise MethodError就可以抛出相应的异常
# 但是有时候这里定义的errmsg可能不适合所有场景，
# 那么可以通过传入自定义的errmsg来更改
# raise MethodError('别瞎调用我接口')
class BaseError(Exception):
    errno = 10000
    errmsg = '程序员跑路了'

    def __init__(self, errmsg=None):
        if errmsg:
            self.errmsg = errmsg


class MethodError(BaseError):
    errno = 10001
    errmsg = '不支持的请求方式'


class LoginError(BaseError):
    errno = 11001
    errmsg = '用户名或密码错误'
