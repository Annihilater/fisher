#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/1 01:05
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : admin_reset_pwd.py
from app import db
from app.models.user import User
from fisher import app


def admin_reset_password(uid, raw):  # 仅供开发的时候修改账户密码使用
    with db.auto_commit():
        user = User.query.get_or_404(uid)
        user.password = raw


if __name__ == '__main__':
    user_id = input('请输入 user.id: ')
    password = '0' * 8

    with app.app_context():
        admin_reset_password(user_id, password)
    print('id为 ' + str(user_id) + ' 的用户密码已重置为 ' + password)
