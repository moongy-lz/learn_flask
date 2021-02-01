#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/26
# @file manager.py
"""
入口文件： 1. 使用 flask_script 来管理整个项目
         2. 使用工厂方法根据开发环境的不同创建对应的 Flask 对象
         3. 进行数据库迁移扩展
"""
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app import create_app, db

# 使用导入 create_app() 函数来根据传入的参数(对应配置模式)来创建一个 Flask 对象
api = create_app('develop')

# 创建 Manager 对象，将创建的 api 作为参数来绑定它是被管理运行的 Flask 对象
manager = Manager(api)

# 将 Flask 对象与创建的 model db 绑定创建为 Migrate 对象，用以进行数据库迁移
Migrate(api, db)

"""
# 数据库迁移命令
    python manager.py db init
    python manager.py db migrate
    python manager.py db upgrade
"""
# 使用 Manager 来管理数据库迁移的操作(作为其运行入口)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
