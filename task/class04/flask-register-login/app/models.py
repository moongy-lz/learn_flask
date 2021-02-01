#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/30
# @file models.py
from datetime import datetime
from app import db

# 这里导入的两个模块用于将注册的用户密码进行加密以及登录时的校验
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'user'
    """
    创建用户登录表
    """
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 用户 id 字段
    mobile = db.Column(db.String(16), unique=True, nullable=False)  # 手机号字段
    nickname = db.Column(db.String(64), unique=True, nullable=False)  # 昵称字段
    password_hash = db.Column(db.String(128), nullable=False)  # 密码字段，需要加密进行存储
    last_login = db.Column(db.DateTime, default=datetime.now)  # 最后一次登录时间， 用于 jwt 认证

    # passpord 方法通过 property 修饰之后,可以当成属性形式调用 设置访问密码的方法,并用装饰器 @property 设置为属性,调用时不用加括号
    # 这里上面的 password_hash 属性可以设置为私有属性吗？？
    @property
    def password(self):
        raise AttributeError('当前属性不可读')  # 当直接读取密码时，报错

    # 设置 setter,可以将用户密码类似属性一样进行传入，然后进行加密
    # 这里加密使用了 werkzeug.security 中的 generate_password_hash 函数来进行加密处理
    # werkzeug.security 中的 check_password_hash 可以相应的进行密码校验操作
    @password.setter
    def password(self, pwd):  # 这里将传入的明文密码作为参数进行加密后存储
        self.password_hash = generate_password_hash(pwd)

    # 设置验证密码的方法，用于登陆时进行校验
    # 传入用户输入的明文密码，明文到 check_password_hash 方法中,如果验证正确返回 True,否则返回 False
    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)

    # 方便读取用户数据
    def to_dict(self):
        return {
            'nickname': self.nickname,
            'mobile': self.mobile
        }



class Books(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 书籍 id 字段
    name = db.Column(db.String(64), unique=True, nullable=False)  # 图书名字段
    category = db.Column(db.String(64))  # 图书类别字段
    price = db.Column(db.Float)  # 书记价格字段
    status = db.Column(db.Enum('0', '1'), default='1')  # 0 是删除状态 1 是存活状态    默认为 1
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 使用外键关联用户表
    owner = db.relationship('User', backref=db.backref('books'))  # 反向引用 backref 找到用户的所有书籍

    # 定义返回的数据字典，方便接口读取数据
    def to_dict(self):
        return {
            'name': self.name,
            'category': self.category,
            'price': self.price,
        }
