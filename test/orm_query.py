#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/2/27 19:02
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : orm_query.py
from sqlalchemy import func, text

from app.models.base import db
from app.models.gift import Gift
from fisher import app

if __name__ == '__main__':
    with app.app_context():
        recent_gift = db.session.query(Gift).filter(
            Gift.launched == False, Gift.status == 1).all()

        print(recent_gift)
        a = 1
