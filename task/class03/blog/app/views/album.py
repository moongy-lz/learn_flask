# 引入渲染模块(使用的是jinja2)，json处理模块，request模块(处理 GET 和 POST 的数据)
from flask import Blueprint, render_template 

album_lz = Blueprint('album', __name__, url_prefix='/album')

@album_lz.route('/')
def album():
    return render_template('html/album.html', data={'api': 'album'})