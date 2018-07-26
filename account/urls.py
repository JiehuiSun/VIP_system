# 这里将url进行统一的管理，每添加一个接口，只需要在urls中添加即可
from flask import Blueprint

from account.views.login.login_view import Login, Register

instance = Blueprint('mod_login', __name__)

urls = ()

# login
urls += (
    ('/login', Login.as_view("login")),
    ('/register', Register.as_view("register")),
)

methods = ['GET', 'POST']
for path, view in urls:
    instance.add_url_rule(path, view_func=view, methods=methods)
