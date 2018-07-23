# 根据需求定义不同model
# username/email/phone没有做数据库级的唯一约束
# 因此需要在程序中进行限制, 为了解决用户删除后，再创建同样的用户问题
from vip_system import db
from utils import time_utils


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128))
    phone = db.Column(db.String(32))
    is_deleted = db.Column(db.Boolean, default=False)
    create_dt = db.Column(db.DateTime, default=time_utils.now_dt)
    update_dt = db.Column(db.DateTime, default=time_utils.now_dt)
