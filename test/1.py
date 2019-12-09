#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/2/26 14:19
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : 1.py

from werkzeug.local import LocalStack


s = LocalStack()
s.push(1)

print(s.top)
print(s.top)
print(s.pop())
print(s.top)


s.push(1)
s.push(2)

print(s.top)
print(s.top)
print(s.pop())
print(s.top)
