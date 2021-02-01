#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/27
# @file __init__.py
from flask import Flask, render_template

from config import configs


# 使用工厂方法创建 Flask 对象
def create_app(config_name):
    app = Flask(__name__)
    config = configs[config_name]
    app.config.from_object(config)

    @app.route('/login')
    def index():
        return 'login'

    return app
