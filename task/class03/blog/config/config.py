"""
根据不同的情况选择不同的配置对象；
开发期间，设置 DEBUG = True，且数据库链接为本地
生产环境中：DEBUG = False， 数据库设置为真实数据库链接
"""
class BaseConfig(object):
    DEBUG = False
    JSON_AS_ASCII = False
    SECRET_KEY = 'shduadhuenfah'


class ProductionConfig(BaseConfig):
    pass


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    # 创建数据库的链接
    # root:mysql@127.0.0.1:3306 这里的 mysql 是设置的数据库连接密码
    # 数据库迁移之前需要先创建好
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:mysql@127.0.0.1:3306/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = False