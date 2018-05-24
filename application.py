import os
import logging
from flask import Flask
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

from easy_flask import configs
from account import account_router
from easy_flask import db
from easy_flask import redis
from easy_flask import session


APP_NAME = 'easy_flask'


def create_app():
    app = Flask(APP_NAME)
    app.config.from_object(configs.DefaultConfig)
    config_blueprint(app)
    config_logger(app)
    config_db(app)
    config_redis(app)
    config_session(app)
    return app


def config_blueprint(app):
    app.register_blueprint(account_router, url_prefix='/api/v1')


def config_logger(app):
    log_dir = './var/log/'
    log_filename = 'flask.log'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    config_dict = {
        'filename': log_dir + log_filename,
    }
    logging.basicConfig(**config_dict)


def config_db(app):
    db.init_app(app)


def config_redis(app):
    redis.init_app(app)


def config_session(app):
    session.init_app(app)


app = create_app()
