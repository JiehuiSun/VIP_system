# 根据用户信息，使用jwt生成token返回给客户端，
# 以后前后端交互都使用此token
# payload中可以添加一个过期时间，或者在redis中做过期都可以
# 这里redis，可以通过传入或者在session中配置
# init_app是flask特有的一种实现单例的方式
import time
import jwt
from redis import StrictRedis


class Session(object):
    REDIS_URI = 'redis://:@localhost:6379/9'
    ALGORITHM = 'HS256'

    def __init__(self, app=None, redis_client=None):
        if redis_client:
            self.redis_client = redis_client
        else:
            self.redis_client = StrictRedis.from_url(self.REDIS_URI)
        if app:
            self.init_app(app)
    def init_app(self, app):
        self.secret_key = app.config.get('SECRET_KEY')
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['session'] = self

    def set_session(self, user_id):
        payload = {
            'user_id': user_id,
            'timestamp': time.time(),
        }
        token = jwt.encode(payload, self.secret_key, self.ALGORITHM).decode()
        self.redis_client.set(token, user_id)

        return token

    def get_session(self, token):
        s = self.redis_client.get(token.encode())
        if not s:
            return
        payload = jwt.decode(token, self.secret_key, self.ALGORITHM)
        user_id = payload.get('user_id')

        return user_id

    def clear_session(self, token):
        self.redis_client.delete(token)
