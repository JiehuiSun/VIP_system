# 将redis封装成flask单例使用模式
from redis import StrictRedis


class FlaskRedis(object):

    def __init__(self, app=None):
        if app:
            self.init_app(app)

    def init_app(self, app):
        redis_url = app.config.get('REDIS_URI')
        self.client = StrictRedis.from_url(redis_url)
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['redis'] = self
