#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/26
# @file passport.py

from flask import url_for, redirect, request, jsonify

from app import db
from app.models import User
# from app.modules.passport import passport_blue


@passport_blue.route('/register', methods=['GET', 'POST'])
def register():
    """
    获取参数
    获取到的参数可以进行校验是否为空或者手机号格式校验等
    创建用户对象(映射数据库中的一条记录)
    将用户的密码进行加密后保存到数据库中(加密可以使用 )
    返回 json 根据不同的结果返回相应的 code 与 msg
    :return 返回 code, msg:
    """
    # 这里使用 url_for 反向生成 url 时，是使用 url_for('passport_blue.register') 来生成

    # 这里注册时传送的数据的几种形式以及相应的读取方法：
    # 1. url 拼接字符串的方式传数据，这个有两种方式进行传递
    # 第一种方式： 以 url 拼接字符串的方式 /index?key=value
    # 使用 request.args() 来获取数据
    # 第二种方式： 以 url 路径的方式进行传递参数 '/index/<int: nid>'
    # 其获取方式为直接将参数作为视图函数的参数进行操作

    # 2. form 表单的提交方式
    # 使用 request.form 来获取表单数据

    # 3. json
    # 第一种读取方式：
    # json_data = request.data  # 先获取 json 字符串数据
    # dict_data = json.loads(json_data)  # 再将 json 字符串数据转换成字典
    # 第二种：
    # dict_data = request.get_json()
    # 第三种：
    dict_data = request.json

    # 获取传来的数据对象中对应的数据
    mobile = dict_data.get('mobile')
    nickname = dict_data.get('nickname')
    password = dict_data.get('password')

    # 对传来的数据进行校验是否为空
    if not all([mobile, password, nickname]):
        return jsonify(code=123, msg='手机号用户名或密码不能为空')  # code

    # 创建用户对象,即与数据库进行映射，以将用户信息保存到数据库中
    user = User()
    user.mobile = mobile
    user.nickname = nickname
    # 注册时拿到的用户密码需要加密存储在数据库中
    # 可以将加密的函数作为 User() 对象方法，集成到 User 类中，这里只需要将 password 明文作为参数即可
    # 这里虽然是对象方法，但可以使用装饰器 @property 来作为属性的形式调用，或者用 __setattr__
    user.password = password

    # 将用户信息保存到 orm 对象中后，进行数据库更新
    # 这里可以将数据更新的函数集成为对象方法， 集成到 User 类中，当进行数据更新时，可以直接调用
    try:
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        return jsonify(code=234, msg='注册失败')

    # 返回前端页面注册成功信息
    return jsonify(code=200, msg='注册成功！')


@passport_blue.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录时，同样地我们从前端拿到用户输入地用户名和密码等数据
    我们在后端要进行地操作为：
    1. 获取参数
    2. 校验参数
    3. 通过手机号或者用户名取出用户对象
    4. 判断用户对象是否存在
    5. 判断用户输入的密码是否与数据库中的密码匹配
    6，记录用户登录的状态
    7. 返回 json 状态码以及登陆提示
    :return:
    """
    # 1. 获取参数
    dict_data = request.json
    mobile = dict_data.get('mobile')
    password = dict_data.get('password')

    # 2. 校验信息
    if not all([mobile, password]):
        return jsonify(code=123, msg='手机号用户名或密码不能为空')
    return 'login'

    # 3.通过手机号或者用户名取出用户对象
    try:
        user = User.query.filter(User.mobile == mobile).first()
    except Exception as e:
        return jsonify(code=123, msg='这个手机号还未注册')

    # 4. 判断用户对象是否存在
    if not user:
        return jsonify(code=124, msg='用户不存在')

    # 5. 判断密码是否正确
    # 这里使用的是 User 中定义的验证方法，传入密码明文来加密匹配
    if not user.check_password(password):
        return jsonify(code=123, msg='手机号或密码输入错误')

    # 6. 记录用户登录的状态
    # 使用 session 来保存会话状态
    session['user_id'] = user.id
    session['mobile'] = user.mobile

    # 7. 返回 json 状态码以及登陆提示
    return jsonify(code=200, msg='登陆成功')
    # obj = request.form()
    # user = obj.get('name')
    # pwd = obj.get('password')
