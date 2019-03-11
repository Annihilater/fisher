from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.libs.email import send_email
from app.models.base import db
from app.models.user import User
from app.web import web


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)  # 实例化注册表单，获取用户提交的表单
    if request.method == 'POST' and form.validate():
        with db.auto_commit():  # 使用@contextmanager重构代码
            user = User()  # 实例化用户
            user.set_attrs(form.data)  # 将真实用户与服务器用户绑定，相应属性赋值
            db.session.add(user)
        # db.session.commit()                             # 将用户数据写入到数据库
        send_email(form.email.data, '注册', 'email_has_send.html')
        flash('一封邮件已发往你的注册邮箱，请及时查收')
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')

    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)

    if request.method == 'POST' and form.validate():
        account_email = form.email.data
        user = User.query.filter_by(email=account_email).first_or_404()
        send_email(
            form.email.data,
            '重置你的密码',
            'email/reset_password.html',
            user=user,
            token=user.generate_token())
        flash('密码重置邮件已经发送到您的邮箱' + account_email + '，请及时查收!')
        return redirect(url_for('web.login'))

    return render_template('auth/forget_password_request.html')


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)

    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('密码重置成功，请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')

    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    return render_template('auth/change_password.html')


@web.route('/logout')
def logout():
    logout_user()
    # logout_user 其实就是将浏览器的 cookie 清空
    return redirect(url_for('web.index'))
