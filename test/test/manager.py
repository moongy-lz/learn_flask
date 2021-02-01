#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/27
# @file manager.py
from flask_script import Manager

from app import create_app

app = create_app('develop')
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
