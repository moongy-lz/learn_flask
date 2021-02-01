#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/27
# @file Werkzeug.py

# Flask 是使用 Werkzeug 来对 Socket 数据进行初步处理的

# from werkzeug import run_simple
#
#
# def func(environ, start_response):
#     print('请求来了')
#     pass
#
#
# if __name__ == '__main__':
#     run_simple('127.0.0.1', 5000, func)


# 在 Flask 中底层就是使用 werkzeug 模块来进行访问请求的 Socket 的数据的初始处理
from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple


# hello 是一个函数，参数为一个请求
@Request.application
def hello(request):
    print('请求来了')
    return Response('Hello World!')


if __name__ == "__main__":
    # 请求一旦到来，执行第三个参数  参数()
    run_simple('localhost', 4000, hello)  # 执行 hello(xxx)
