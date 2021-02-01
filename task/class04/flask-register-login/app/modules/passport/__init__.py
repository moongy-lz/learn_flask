#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/26
# @file __init__.py.py

from flask import Blueprint
from flask_restful import Api

from app.modules.passport.views import Login, Register

# 创建蓝图，路由分发
passport_blue = Blueprint('passport', __name__, url_prefix='/passport')

# 创建 Api 对象
api = Api(passport_blue)

# 将创建好的接口与 Api 对象进行绑定，并且设定其 url
api.add_resource(Login, '/login')
api.add_resource(Register, '/register')

################## 其他方式 ################

# from flask import Blueprint
# from flask_restful import Api
#
# # 创建蓝图对象，用于分发路由
# jwt_passport_blue = Blueprint('jwt_passport', __name__, url_prefix='/jwt_passport')
#
# # 这里要将视图函数所在的文件导入，否则程序找不到路由
# from . import jwt_passport


# from flask import Blueprint

# # 创建蓝图对象，用于分发路由
# passport_blue = Blueprint('passport', __name__)
#
# # 这里要将视图函数所在的文件导入，否则程序找不到路由
# from . import passport
