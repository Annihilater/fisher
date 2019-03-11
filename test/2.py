#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date  : 2019/2/26 14:20
# @Author: PythonVampire
# @email : vampire@ivamp.cn
# @File  : 2.py
import threading
import time

from werkzeug.local import LocalStack

my_stack = LocalStack()  # 实例化具有线程隔离属性的LocalStack对象
my_stack.push(1)
print('in main thread after push, value is:' + str(my_stack.top))


def worker():
    # 新线程
    print('in new thread before push, value is:' + str(my_stack.top))
    # 因为线程隔离，所以在主线程中推入1跟其他线程无关，故新线程中的栈顶是没有值的（None）
    my_stack.push(2)
    print('in new thread after push, value is:' + str(my_stack.top))


new_t = threading.Thread(target=worker, name='my_new_thread')
new_t.start()
time.sleep(1)

# 主线程
print('finally, in main thread value is:' + str(my_stack.top))
# 因为线程隔离，在新线程中推入2不影响主线程栈顶值得打印
