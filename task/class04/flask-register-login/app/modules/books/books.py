#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/26
# @file books.py
from flask import jsonify, request, g
from flask_restful import Resource
from app import db
from app.models import Books


# 创建接口类
class BooksView(Resource):
    """
    获取所有书籍的接口
    """

    def get(self):
        # 获取书籍状态存活的书籍，即现在存有的书籍
        books = Books.query.filter(Books.status == '1').all()

        return jsonify(code=200, msg='获取书籍列表成功', data=[i.to_dict() for i in books])

    def post(self):
        data_dict = request.json  # 获取发送的 json 数据
        name = data_dict.get('name')
        category = data_dict.get('category')
        price = data_dict.get('price')
        user_id = g.user.id

        # 将用户信息存入数据库
        book = Books()
        book.name = name
        book.category = category
        book.price = price
        # 将用户 id 直接赋值给 user_id
        book.user_id = user_id

        try:
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            return jsonify(code=400, msg='数据跟新失败')

        return jsonify(code=200, msg='添加书籍成功', data=book.to_dict())


class BookView(Resource):
    """
    对某一本书进行操作的接口
    """

    def get(self, book_id):
        # 获取指定的书籍
        book = Books.query.get(book_id)
        if not book:
            return jsonify(code=123, msg='您所查询的书籍并不存在 ')

        return jsonify(code=200, msg='您所查询的书籍已找到', data=book.to_dict())

    def put(self, book_id):
        data_dict = request.json
        book = Books.query.get(book_id)

        # 判断书籍的 user_id 与 登录用户的 id 是否匹配
        if not book.user_id == g.user.id:
            return jsonify(code=123, msg="您不能修改他人的书籍")
        if not book:
            return jsonify(code=123, msg="您所查询的书籍并不存在")
        if book.status == '0':
            return jsonify(code=123, msg="您所查询的书籍已删除")
        book.category = data_dict.get('category')
        book.price = data_dict.get('price')
        from app.models import db

        try:
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            return jsonify(code=400, msg='数据跟新失败')
        return jsonify(code=200, msg='更新成功', data=book.to_dict())

    def delete(self, book_id):
        book = Books.query.get(book_id)

        # 判断书籍的 user_id 与 登录用户的 id 是否匹配
        if not book.user_id == g.user.id:
            return jsonify(code=123, msg="您不能修改他人的书籍")
        if not book:
            return jsonify(code=400, msg="您所查询的书籍并不存在")
        if book.status == '0':
            return jsonify(code=400, msg="您所查询的书籍已删除")
        book.status = '0'

        try:
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            return jsonify(code=400, msg='数据跟新失败')
        return jsonify(code=200, msg='删除成功')
