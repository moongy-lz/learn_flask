#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/26
# @file config.py
import redis
# import os


class BaseConfig(object):
    # 调试模式开启
    DEBUG = True
    # 让 jsonify 返回的 json 字符串支持中文显示
    JOSN_AS_ASCII = False
    # 配置密钥字符串，给 session 还有其他的签名算法使用
    # 通过 os.urandom(24) 可以获取相对强壮的密钥
    # SECRET_KEY = os.urandom(24)  # 这里每次连接都会生成随机字符串的话，那么如何验证？应该为每次链接保存其值吗？
    SECRET_KEY = 'sauifhauhwefba'

    # 创建数据库的链接
    # root:mysql@127.0.0.1:3306 这里的 mysql 是设置的数据库连接密码
    # 数据库迁移之前需要先创建好
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@127.0.0.1:3306/restful'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 配置 redis 数据库信息， redis 模块不是 Flask 的扩展，不会自动从 config 中读取配置信息，需要自己读取
    # 也就是说，这里的 redis 配置变量，需要在使用时导入使用
    REDIS_HOST = '127.0.0.1'  # 本地地址
    REDIS_PORT = 6379  # redis 一般默认设置为此端口
    REDIS_PASSWORD = '12345'  # 我在本地安装 redis 时设置了一个简单密码

    # flask-session 的配置信息
    SESSION_TYPE = 'redis'  # 将 session 信息保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id(uuid4()) 被签名加密后存储
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)  # 绑定 redis 数据库的地址端口
    PERMANENT_SESSION_LIFETIME = 24 * 30 * 30  # session 的有效期， 单位是秒，默认是31天


class DevelopConfig(BaseConfig):
    """
    开发环境下的配置与基础配置类相同
    """
    pass


class ProductionConfig(BaseConfig):
    """生产环境"""
    DEBUG = False

    # 生产环境的数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@127.0.0.1:3306/reestful'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # redis 数据库的生产环境配置
    REDIS_HOST = '127.0.0.1'  # 本地地址
    REDIS_PORT = 6379  # redis 一般默认设置为此端口


class TestingConfig(BaseConfig):
    """测试环境"""
    TESTING = True


# 将上述定义的配置类写在字典中，并将其导入 app ，创建 Flask 对象时可以从字典中获取配置类
# 这样就可以在多个环境中切换，只需要更改相应的配置类就可以
configs = {
    'develop': DevelopConfig,
    'produce': ProductionConfig,
    'test': TestingConfig
}
