#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/26
# @file __init__.py.py

from flask import Blueprint, request, jsonify
from flask_restful import Api
from app.utils.auth import Auth

books_blue = Blueprint('books', __name__, url_prefix='/books')


@books_blue.before_request
def bedore_request():
    """
    这里要求在登录后才进行数据库的相关操作，所以在这里进行验证
    在蓝图上设置 before_request，进行认证操作，只影响蓝图对象绑定的请求
    导入 auth 模块使用 jwt 来做验证操作
    :return json:
    """
    result = Auth().identify(request)
    if result['code'] == 200:
        # 在创建 app 时，添加反爬功能时已经使用 g 绑定了 user, 这里可以不用设置了
        # g.user = User.query
        return
    else:
        return jsonify(code=123, msg='用户未登录，没有权限进行访问')


# 创建 Api 对象
api = Api(books_blue)

# 导入创建好的 resource 接口类
from app.modules.books.books import BooksView, BookView

# 将创建好的接口与 Api 对象进行绑定，并且设定其 url
api.add_resource(BooksView, '/v1/books')
api.add_resource(BookView, '/v1/book/<int:book_id>')  # 根据 url 的参数确定书籍 id
