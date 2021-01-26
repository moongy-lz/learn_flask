"""
创建一个装饰器，用来验证是否处在登录状态
:view_func: 被修饰的视图函数，即需要判断登录状态的视图函数
:return: 如果是登录状态，则继续运行视图函数，否则
"""
import functools
from flask import session, g

def user_login_state(func):
    @functools.wraps(func)   # 这里必须使用 functools.wraps 来绑定原函数的信息，否则可能会出现路由问题
    def wrapper(*args, **kwargs):
        # 获取用户
        user_id = session.get('user_id')
        # 这里为什么要将 user 设置为 None
        user = None
        if user_id:
            from app.models import User
            user = User.query.get(user_id)

        # 将 user 对象存入全局变量中
        g.user = user
        return func(*args, **kwargs)

    return wrapper
