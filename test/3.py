#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/3/7 18:49
# @Author: yanmiexingkong
# @email : yanmiexingkong@gmail.com
# @File  : 3.py
import re

s = "386 页"
r = re.findall("(\d*).*", s)[0]
print(r)
