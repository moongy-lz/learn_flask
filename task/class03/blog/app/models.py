from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64))
    ip = db.Column(db.String(64))
    login_time = db.Column(db.DateTime, default=datetime.now)

class Content(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True, nullable=False)
    src = db.Column(db.String(255))
    p = db.Column(db.String(1024))
    title = db.Column(db.String(128))
    tag = db.Column(db.String(128))
    video = db.Column(db.String(255))

    # 创建 to_dict 方法，直接将数据库中的数据进行格式化操作，
    # 此处为将数据添加到字典中，以此传递数据时可以进行相应操作
    def to_dict(self):
        # 返回对象的 字段值
        return {
            'id': self.id,
            'src': self.src,
            'p': self.p,
            'title': self.title,
            'tag': self.tag,
            'video': self.video
        }