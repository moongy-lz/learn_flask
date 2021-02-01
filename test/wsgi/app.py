#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/27
# @file app.py

from werkzeug import run_simple


# Flask 实际上就是在 werkzeug 基础上封装成一个对象
class Flask(object):

    def __call__(self, environ, start_response):
        return 'xx'

    def run(self):
        # 这里就调用 werkzeug 中的 run_simple 方法来进行响应
        run_simple('127.0.0.1', 5000, self)


app = Flask()

if __name__ == '__main__':
    # 这里运行的对象的 run() 方法，其内部调用的还是 werkzeug 模块的 run_simple 函数
    # 其 run_simple 函数的第三个参数是对象 self 自己，这样它又继续调用其 __call__ 方法
    app.run()
