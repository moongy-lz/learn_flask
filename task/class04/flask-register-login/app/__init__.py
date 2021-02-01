#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/26
# @file __init__.py.py

from flask import Flask, request, g, current_app, jsonify
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis
from flask_session import Session
# from app.utils.auth import Auth  Auth要使用 db 模块，所以要放在下面
from config.config import configs  # 导入配置文件中定义的配置对象字典

# session 除了保存用户会话信息，也可以保存其他的信息
db = SQLAlchemy()  # 创建 SQLAlchemy 对象，先创建 SQLAlchemy 对象，再和 Flask 对象进行关联
redis_store = None


def create_app(config_name):
    """
    根据参数选择不同的配置来创建app的工厂方法
    :param config_name:
    :return app:
    """
    # Flask 对象是必须要创建的
    app = Flask(__name__)
    # 根据创建 app 时输入的参数 config_name 来获取配置类
    config = configs[config_name]
    # 对 Flask 对象 app 进行环境配置
    app.config.from_object(config)

    # db = SQLAlchemy(app)  # 创建连接到 MySQL 数据库的对象
    db.init_app(app)  # 将上面的形式写成这样可以避免循环导包的发生，上面的代码实际上底层的实现就是这样的

    # 创建一个全局变量
    global redis_store
    # 创建一个 redis 连接对象
    # 因为redis取出来的数据是二进制，decode_responses让响应转为字符串
    redis_store = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, password=config.REDIS_PASSWORD,
                              decode_responses=True)
    # 创建 Session 对象，绑定 app， 指定 session 数据保存的位置
    # 保存的位置和相关设置就是在配置文件中设置的 SESSION_TYPE SESSION_USE_SIGNER SESSION_REDIS PERMANENT_SESSION_LIFETIME
    # 这里的 SESSION_TYPE 可以是 redis memcached filesystem mongodb sqlalchemy
    # 源码中也是 self.init_app(app) 与上面的 SQLAlchemy(app) 相同
    # 这里如果不需要存储 session 信息时， 只要将 Session(app) 注释掉就可以了，我们在工作中编程时，也应该注重解耦的应用
    Session(app)
    from app.utils.auth import Auth

    @app.before_request
    def before_request():
        # 这里使用的是 jwt, 数据用户 id 从 jwt 中读取
        user_id = Auth().get_jwt_data(request)
        if user_id:
            from app.models import User
            # g 是在 before_request 之前创建的
            g.user = User.query.get(user_id)
            # count 变量用于计数
            count = 0
            # 从缓存中查询请求次数
            try:
                count = redis_store.get("request_count:%s" % user_id) or 0
            except Exception as e:
                # current_app 与 g 是同时创建的，生命周期相同
                # 将报错信息记录在 current_app.logger，这里不能 return 否则程序会被阻断
                current_app.logger.error(e)

            if isinstance(count, str):
                count = int(count)

                # 如果次数大于20,直接不让用户再继续了
                # 这里只能等 redis 刷新之后再继续了
                if count >= 20:
                    return jsonify(code=1234, msg='请求过于频繁，请稍后尝试')

                # count 计数，每次登录时自增 1
                count += 1
                try:
                    # 在 redis 中添加数据 user_id count 以及 redis 请求次数有效时间，单位是秒
                    redis_store.set("request_count:%s" % user_id, count, 5)
                except Exception as e:
                    current_app.logger.error(e)

                # 判断用户请求是否包含有浏览器(软件信息以及 http 版本信息等)信息，不过没有，则判定为爬虫
                if not request.user_agent:
                    return jsonify('不是浏览器请求，可能是爬虫')
        return

    # 在 Flask 对象上绑定创建的蓝图对象，这里不是模块文件
    from app.modules.books import books_blue
    app.register_blueprint(books_blue)

    # 使用 jwt 来做验证功能
    from app.modules.passport import passport_blue
    app.register_blueprint(passport_blue)

    return app
