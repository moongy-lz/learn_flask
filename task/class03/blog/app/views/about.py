# 引入渲染模块(使用的是jinja2)，json处理模块，request模块(处理 GET 和 POST 的数据)
from flask import Blueprint, render_template 

about_lz = Blueprint('about', __name__, url_prefix='/about')

@about_lz.route('/')
def about():
    return render_template('html/about.html', data={'api': 'about'})