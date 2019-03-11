from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from app import mail


def send_async_email(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            return 404


def send_email(to, subject, template, **kwargs):
    # def send_email():
    #     msg = Message('测试邮件', sender='schip@qq.com', body='Test',
    #                   recipients=['schip@qq.com'])
    msg = Message('鱼书' + '' + subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template, **kwargs)
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()

    # mail.send(msg)
    # 发送邮件

# def send_email(to, subject, template, **kwargs):
#     msg = Message('鱼书'+''+ subject,
#                   sender=current_app.config['MAIL_USERNAME'],
#                   recipients=[to])
#     msg.html = render_template(template, **kwargs)
#     thr = Thread(target=send_async_email, args=[current_app, msg])
#     thr.start()
