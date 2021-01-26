# 引入渲染模块(使用的是jinja2)，json处理模块，request模块(处理 GET 和 POST 的数据)
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, session, g
from app.models import User
from app.utils.common import user_login_state

# 创建 admin_lz 的蓝图，用于管理 admin 相关的视图函数接口
admin_lz = Blueprint('admin', __name__, url_prefix='/admin')

# admin 的主页视图函数
@admin_lz.route('/')
@user_login_state   # 自己创建的装饰器要放在路由的下方
def index():
    # 判断用户是否已经登录，如果登录，则显示主页，没有登录则转到登陆页面
    # 用户登录时，将用户信息保存在 session 中，以进行判断，
    # 请求结束时，会将 session 信息保存到 cookie 中，以进行多次连接的验证
    # user_id = session.get('user_id')  # 读取 session 中的用户数据
    if g.user:  # 判断 session 用户信息是否存在
        return render_template('X-admin/index.html')

    # 如果没有对应的用户信息，即没有登录，则返回登录页面
    return redirect(url_for('admin.login'))

@admin_lz.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('X-admin/login.html')

    """ 使用 form 获取数据进行登录

    # 这里 form 表单可以获取到，但是 json 对象获取不到
    # 原因是 ajax 使用了 id 属性获取对象，而之前并没有在 form 上设置 id 属性
    data_dict = request.form
    username = data_dict.get('username')
    password = data_dict.get('password')
    # print(username, password)
    # 从数据库中查询相对应的用户名，能够查询匹配则查询其密码是否匹配
    user = User.query.filter_by(name=username).first()
    if not user:
        return jsonify(code=400, msg='没有用户')
    if password != user.password:
        return jsonify(code=400, msg='密码错误')
    # 登录成功后，将用户信息保存在 session 中，以进行登录状态的判断
    # 另外要注意点的一点是，要使用 session，需要在 app(Flask对象) 上添加 SECRET_KEY，用以加盐加密
    session['user_id'] = user.id
    session['user_name'] = user.name
    return jsonify(code=200, msg='登录成功')

    """
    # login 中的 form 设置了 id 属性值之后，就可以收到 .json 数据了，
    # 对数据的处理基本与之前是相同的
    data_dict = request.json
    print(data_dict) 
    username = data_dict.get('username')
    password = data_dict.get('password')
    user = User.query.filter_by(name=username).first()

    if not user:
        return jsonify(code=400, msg='没有用户')

    if password != user.password:
        return jsonify(code=400, msg='密码错误')

    session['user_id'] = user.id
    session['user_name'] = user.name
    return jsonify(code=200, msg='登录成功')



@admin_lz.route('/logout', methods=['GET', 'POST'])
def logput():
    # 登出时，删除 session 中的用户信息
    session.pop('user_id')
    session.pop('user_name')
    return redirect(url_for('admin.login'))

# 获取失败，原 html 文件的指向路径不正确导致的
@admin_lz.route('/welcome', methods=['GET', 'POST'])
@user_login_state  # 有了这个就有了 g
def welcome():
    return render_template('X-admin/welcome.html')