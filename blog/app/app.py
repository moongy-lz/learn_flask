#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/26
# @file app.py.py

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'Index'


if __name__ == '__main__':
    app.run()
