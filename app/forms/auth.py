from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo

from app.models.user import User


class EmailForm(Form):
    email = StringField(
        validators=[DataRequired(), Length(8, 64), Email(message="电子邮件不符合规范")]
    )


class LoginForm(EmailForm):
    password = PasswordField(
        validators=[DataRequired(message="密码不可以为空,请输入你的密码"), Length(6, 32)]
    )

    # def validate_email(self, field):
    #     if not User.query.filter_by(email=field.data).first():
    #         raise ValidationError('该邮箱未被注册')
    #
    # def validate_password(self, field):
    #     if User.query.filter_by(password=field.data) != field.data:
    #         raise ValidationError('密码错误')


class RegisterForm(LoginForm):
    nickname = StringField(
        validators=[DataRequired(), Length(2, 10, message="昵称至少需要两个字符，最多10个字符")]
    )

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("电子邮件已被注册")

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError("该昵称已被注册")


class ResetPasswordForm(Form):
    password1 = PasswordField(
        validators=[
            DataRequired(),
            Length(6, 32, message="密码长度至少需要在6到32个字符之间"),
            EqualTo("password2", message="两次输入的密码不相同"),
        ]
    )
    password2 = PasswordField(validators=[DataRequired(), Length(6, 32)])
