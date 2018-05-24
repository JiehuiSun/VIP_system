# 这里将url进行统一的管理，每添加一个接口，只需要在urls中添加即可
from flask import Blueprint

from .views import Login

account_router = Blueprint('account', __name__, url_prefix='/account')

urls = (
    ('/login', Login()),
)

methods = ['GET', 'POST']
for path, view in urls:
    account_router.add_url_rule(path, view_func=view, methods=methods)
