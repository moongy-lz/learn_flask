# 引入渲染模块(使用的是jinja2)，json处理模块，request模块(处理 GET 和 POST 的数据)
from flask import Blueprint, render_template 

leacots_lz = Blueprint('leacots', __name__, url_prefix='/leacots')

@leacots_lz.route('/')
def leacots():
    return render_template('html/leacots.html', data={'api': 'leacots'})