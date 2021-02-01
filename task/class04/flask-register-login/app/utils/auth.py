#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/2/1
# @file auth.py

import datetime
import jwt
import time

from flask import jsonify
from app import db
from config.config import BaseConfig
from app.models import User


class Auth(object):
    # 静态方法用于加密和解密 jwt Token 信息, 对象方法作为接口进行使用
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        使用 jwt 生成 Token 信息，将 user_id 与 login_time 作为参数来生成 Token
        :param user_id:
        :param login_time:
        :return:
        """
        try:
            # 设置 jwt payload 载荷信息
            payload = {
                # 标准中注册的声明
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=20),  # 过期时间，要大于签发时间 20分钟
                'iat': datetime.datetime.utcnow(),  # 签发时间
                'iss': 'lizhen',  # 签发者 自定义
                # 将 uer_id 与 login_time 作为私有声明的信息
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            # 返回 jwt 生成的 Token(以下三部分为 header payload secret)
            return jwt.encode(
                payload,  # jwt 加载的数据
                BaseConfig.SECRET_KEY,  # 设置的 salt，用于生成签名加密
                algorithm='HS256'  # 这里是 header信息，表明签名方式
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        在用户登录时对 Token 信息进行简单验证，查看其是否包含 payload 数据以及其 Token 时间是否过期
        验证通过后，返回 payload 信息
        :param auth_token:
        :return payload:
        """
        try:
            payload = jwt.decode(auth_token, BaseConfig.SECRET_KEY, leeway=datetime.timedelta(days=1))
            # 可以通过设置参数取消过期时间验证
            # payload = jwt.decode(auth_token, Config.SECRET_KEY, options={'verify_exp': False})

            # 这里不需要对 id: user_id 进行查询吗？
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    def authenticate(self, mobile, password):
        """
        用户登录信息进行验证，成功后创建并返回 token，并将登录时间写入数据库；
        如果登录失败返回失败原因
        :param mobile:
        :param password:
        :return:
        """
        user = User.query.filter_by(mobile=mobile).first()
        if not user:
            return jsonify(code=111, msg='用户不存在')
        if user.check_password(password):
            login_time = datetime.datetime.now()
            # 将登录的时间写入数据库中，
            user.last_login = login_time
            try:
                db.session.add(user)
                db.session.commit()
            except Exception as e:
                return jsonify(code=234, msg='登录信息未成功加载')
            # 这里的时间需要把登陆时间转化为时间戳的格式
            login_time_stamp = int(time.mktime(datetime.timetuple(login_time)))
            # 生成新的 jwt Token 信息
            token = self.encode_auth_token(user.id, login_time_stamp)
            response_dict = {'code': 200, 'msg': '请求成功', 'token': token.decode()}
            return jsonify(response_dict)
        else:
            return jsonify(code=111, msg='密码错误')

    def identify(self, request):
        """
        用户鉴权: 读取用户请求时携带的 jwt 信息进行验证其 payload 加密信息是否匹配
        这里使用用户鉴权的作用是可以对 Api 访问前进行 Token 信息认证，当用户信息匹配时，则可以继续操作
        :param request:
        :return:
        """
        # 获取header中的Authorization
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token_arr = auth_header.split(" ")  # 将 auth_header 字符串以空格进行分隔
            # 对 auth_token_arr 信息进行判断是否符合 jwt 标准信息形式(以 JWT 为首， 长度为 2)
            if not auth_token_arr or auth_token_arr[0] != 'JWT' or len(auth_token_arr) != 2:
                return jsonify(code=111, msg='验证头信息有误')
            else:
                # 读取 Token 以及内部 payload 的信息
                auth_token = auth_token_arr[1]
                payload = self.decode_auth_token(auth_token)  # 使用上面定义的 decode_auth_token() 方法来获取 payload
                if not isinstance(payload, str):
                    # 从 data 字典中获取 Token 创建时写入的 user_id 和 login_time 信息
                    user_id = payload.get('data').get('id')
                    login_time = payload.get('data').get('login_time')
                    # 查询数据中的 user_id 信息，能够匹配则认证成功
                    user = User.query.get(user_id)
                    if not user:
                        return jsonify(code=111, msg='验证头信息有误')
                    else:
                        # 这里对登录时间的判断可以实现单点登录的功能
                        if user.last_login == login_time:
                            response_dict = {'code': 200, 'msg': '请求成功', 'user_id': user.id}
                            return response_dict
                        else:
                            return jsonify(code=111, msg='用户认证失败')
                else:
                    return jsonify(code=111, msg='用户认证失败')
        else:
            return jsonify(code=111, msg='用户认证失败')

    def get_jwt_data(self, request):
        """
        从 request 中获取 jwt 中保存的 user_id,用于在做反爬功能的时候使用
        :param request:
        :return user_id:
        """
        auth_header = request.headers.get('Authorization')  # 从 'Authorization' 中读取 jwt 信息
        if auth_header:
            auth_token_arr = auth_header.split(" ")  # 将 jwt 的信息进行拆分
            auth_token = auth_token_arr[1]  # 解析 jwt 数据
            payload = self.decode_auth_token(auth_token)  # 获取 payload 信息
            user_id = payload.get('data').get('id')  # 读取 user_id 信息
            return user_id  # 返回 user_id 信息

        return
