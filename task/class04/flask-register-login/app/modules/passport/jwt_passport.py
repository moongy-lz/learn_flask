#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/31
# @file jwt_passport.py

from flask import request, jsonify

from app import db
from app.models import User
from app.modules.passport import jwt_passport_blue
from app.utils.auth import Auth


@jwt_passport_blue.route('/register_jwt', methods=['GET', 'POST'])
def register():
    """
    用户注册模块，流程与 passport.py 相同
    :return 返回 code, msg:
    """
    data_dict = request.json

    # 获取传来的数据对象中对应的数据
    mobile = data_dict.get('mobile')
    nickname = data_dict.get('nickname')
    password = data_dict.get('password')

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


@jwt_passport_blue.route('/login_jwt', methods=['GET', 'POST'])
def login():
    # 1.获取参数
    dict_data = request.json
    mobile = dict_data.get("mobile")
    password = dict_data.get("password")

    # 2.校验参数
    if not all([mobile, password]):
        return jsonify(code=123, msg='手机号用户名或密码不能为空')

    # 使用 Auth 模块中 jwt Token 进行认证， 将 mobile 与 password 信息作为参数进行验证
    # 验证通过后会返回 jwt Token
    return Auth().authenticate(mobile, password)


@jwt_passport_blue.route('/user', methods=['GET'])
def user():
    """
    获取用户信息
    :return: json
    """
    # 进行 jwt 验证，验证通过后返回访问信息
    result = Auth().identify(request)

    if result['code'] == 200:
        user = User.query.get(result.get('user_id'))
        user_dict = user.to_dict()
        response_dict = {'code': 200, 'msg': '请求成功', 'data': user_dict}
        return jsonify(response_dict)
    else:
        return jsonify(result)
