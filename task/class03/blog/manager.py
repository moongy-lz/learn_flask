# 使用 pip install flask_script, flask_migrate 来安装 
# flask_script 通过命令行的方式来运行程序
# 使用Flask-Migrate扩展，来实现数据迁移
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from app.models import User
from app import app, db

# url_map 路由的设置都是添加到 url_map 中的，可以打印查看
# print(app.url_map)
manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
