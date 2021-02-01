#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @author Moongy
# @date 2021/1/27
# @file app.py
from flask import Flask, render_template, request, redirect, session, url_for
from config import Config
import functools

app = Flask(__name__)
app.config.from_object(Config)
# 使用 session 时，需要设置 secret_key
app.secret_key = 'safsfafsfw'

# 用户信息
DATA_DICT = {
    '1': {'name': '张三', 'age': 32},
    '2': {'name': '李四', 'age': 23},
}


def auth(func):
    
    @functools.wraps(func)
    def inner(*args, **kwargs):
        username = session.get('xxx')
        if not username:
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return inner


@app.route('/index')
@auth
def index():
    # 在访问主页时，先判断是否已登录,即 session 中是否保存有用户信息
    data_dict = DATA_DICT
    print(index.__name__)
    return render_template('index.html', data_dict=data_dict)


# 默认路由只支持 GET 请求，其他请求需要设置
@app.route('/login', methods=['GET', 'POST'])
def login():
    # 判断请求方法， GET 请求返回登录页面， POST 请求可以对传来的数据进行处理
    if request.method == 'GET':
        # 这里模板文件的默认存放位置为 templates，也可以在创建对象处进行设置
        # return '登录'
        # return jsonify({'code':200, 'data': [1, 2, 3]})
        # return render_template('login.html')
        return render_template('login.html')
    # 前端 form 表单中传送 user、pwd 数据时
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    if user == 'moongy' and pwd == '123456':
        session['xxx'] = 'moongy'
        return redirect('/index')
    # 当登录失败时，需要在返回页面中进行提示
    msg = '用户名或密码错误'
    # return render_template('login.html', **{'msg': msg})
    return render_template('login.html', msg=msg)


@app.route('/edit', methods=['GET', 'POST'])
@auth
def edit():
    nid = request.args.get('nid')
    info = DATA_DICT[nid]

    # 这里可以进行编辑页面的操作
    if request.method == 'GET':
        return render_template('edit.html', info=info)

    # 因为 POST 方法默认提交在本页面，所以此时已然能够获取 nid 的值
    user = request.form.get('user')
    age = int(request.form.get('age'))
    print(type(age))
    DATA_DICT[nid]['name'] = user
    DATA_DICT[nid]['age'] = age
    return redirect('/index')


# @app.route('/delete')
# def delete():
#     nid = request.args.get('nid')
#     print(nid)
#     return '删除'

@app.route('/delete/<nid>')
@auth
def delete(nid):
    # nid = request.args.get('nid')
    print(nid)
    # 这里可以进行删除操作,del 删除的是引用，而非数据本身
    del DATA_DICT[nid]
    return redirect('/index')


if __name__ == '__main__':
    app.run()
