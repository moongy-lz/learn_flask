# 引入渲染模块(使用的是jinja2)，json处理模块，request模块(处理 GET 和 POST 的数据)
from flask import Blueprint, render_template, jsonify, request, current_app
from app.models import Content

# 创建 index_lz 的蓝图，用于管理主页相关的视图函数接口
index_lz = Blueprint('index', __name__, url_prefix='/index')

@index_lz.route('/favicon.ico')
def web_logo():
    """
    # 每个网站都会去设置/favicon.ico小logo图标
    # 可以使用current_app.send_static_file(),自动加载static静态文件下面的内容
    :return:
    """
    return current_app.send_static_file("snipaste.ico")

# 主页页面视图函数
@index_lz.route('/')
def index():
    # 数据库 Content 中的数据数量
    count = Content.query.count()
    return render_template('/html/index.html',data={'api': 'index','count': count, 'logs':100, 'read': 1000})

@index_lz.route('/data')  # 这里有前缀在，所以实际在页面中为 /index/data
def data():
    """
    :paginate  page:当前页数 pages:总页数 total:数据总条数 ...
    :return:
    """
    # 页面通过 get 方法传入的参数，传来的都是字符串，需要转化为整型
    page = int(request.args.get('page'))  # 具体的分页值
    pageSize = int(request.args.get('pageSize'))  # 每一页的内容多少

    # 将数据库中的数据提取出来，以便传递到页面
    # contents = Content.query.all()
    paginate = Content.query.paginate(page, pageSize) # 分页对象,其可以获取多个不同属性值
    # count = paginate.total  # 分页对象的总条数
    contents = paginate.items
    # content_list = []
    # 将数据库中的数据按照不同字段形成键值对构成字典，保存到列表中，方便传输
    # 这里传递的对象然后进行操作，可以直接继承到对象中的方法操作，以直接获取相应的数据格式
    # for i in contents:
    #     # content_dict = {}
    #     # content_dict['id'] = i.id
    #     # content_dict['src'] = i.src
    #     # content_dict['p'] = i.p
    #     # content_dict['title'] = i.title
    #     # content_dict['tag'] = i.tag
    #     # content_dict['video'] = i.video

    #     # 也可以直接进行字典赋值再添加
    #     content_dict = {
    #         'id' = i.id,
    #         'src' = i.src,
    #         'p' = i.p,
    #         'title' = i.title,
    #         'tag' = i.tag,
    #         'video' = i.video
    #     }

    #     content_list.append(content_dict)

    # 获取数据库中数据时，使用其自定义的格式化方法来获取
    return jsonify(code=200, msg='complete', data=[i.to_dict() for i in contents])