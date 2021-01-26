# 引入渲染模块(使用的是jinja2)，json处理模块，request模块(处理 GET 和 POST 的数据)
from flask import Blueprint, render_template 

whisper_lz = Blueprint('whisper', __name__, url_prefix='/whisper')

@whisper_lz.route('/')
def whisper():
    return render_template('html/whisper.html', data={'api': 'whisper'})