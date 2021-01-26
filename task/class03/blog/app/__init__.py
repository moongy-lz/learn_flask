from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from config.config import DevelopmentConfig

app = Flask(__name__)

# 创建连接到MySQL数据库的对象
db = SQLAlchemy(app)
# 获取开发环境的配置信息
app.config.from_object(DevelopmentConfig)

@app.route('/')
def index():
    return redirect('/index/')  

# 将创建的首页蓝图对象挂载到 app
from .views.index import index_lz
app.register_blueprint(index_lz)

# 将创建的 admin 蓝图对象挂载到 app
from .views.admin import admin_lz
app.register_blueprint(admin_lz)

# 将创建的 whisper 蓝图对象挂载到 app
from .views.whisper import whisper_lz
app.register_blueprint(whisper_lz)

# 将创建的 leacots 蓝图对象挂载到 app
from .views.leacots import leacots_lz
app.register_blueprint(leacots_lz)

# 将创建的 album 蓝图对象挂载到 app
from .views.album import album_lz
app.register_blueprint(album_lz)

# 将创建的 about 蓝图对象挂载到 app
from .views.about import about_lz
app.register_blueprint(about_lz)