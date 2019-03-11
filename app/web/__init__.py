from flask import Blueprint, render_template

web = Blueprint('web', __name__)


# 将 web 蓝图实例化放在单独的文件里
# 这样可以避免 book 模块导入 web 蓝图的时候进行循环导入


@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


from app.web import auth, book, drift, gift, main, user, wish
# 导入 auth, book, drift, gift, main, user, wish视图函数模块
# 不导入将导致视图函数无法执行
