from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail

from app.models.base import db

login_manager = LoginManager()  # 实例化 LoginManager

mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.secure")
    app.config.from_object("app.setting")

    register_blueprint(app)  # 调用蓝图注册函数

    db.init_app(app)
    # 写法一：传入关键字参数
    # db.create_all(app=app)
    # 写法二：with语句 + 上下文管理器
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)  # 初始化 login_manager
    login_manager.login_view = "web.login"
    login_manager.login_message = "请先登录或注册"

    mail.init_app(app)

    # create_db_table()  # 创建数据表
    return app


def register_blueprint(flask_app):
    from app.web import web

    flask_app.register_blueprint(web)


# def create_db_table():
#     """
#     有几个模型就导入几个模型，
#     前面已经让模型继承了 sqlalchemy 并初始化过了，
#     现在只需要导入才会在数据库中创建数据表
#     :return:
#     """
#     from app.models.book import Book
#     from app.models.drift import Drift
#     from app.models.gift import Gift
#     from app.models.user import User
#     from app.models.wish import Wish
