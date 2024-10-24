# app/models.py

from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import pytz

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(200), default='1.jpg')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    #create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    create_time = db.Column(db.DateTime, index=True, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', name='user_post'), nullable=False)

    author = db.relationship('User', backref=db.backref('posts', lazy='dynamic'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    comment_time = db.Column(db.DateTime, index=True, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', name='comment_post'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', name='comment_user'), nullable=False)

    post = db.relationship('Post', backref=db.backref('comments', lazy='dynamic'))
    author = db.relationship('User', backref=db.backref('comments', lazy='dynamic'))


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, index=True, default=lambda: datetime.now(pytz.timezone('Asia/Shanghai')))

    # 定义 relationship 方便关联查询
    author = db.relationship('User', backref='notifications', lazy=True)
    post = db.relationship('Post', backref='notifications', lazy=True)
    comment = db.relationship('Comment', backref='notifications', lazy=True)

    def __repr__(self):
        return f'<Notification {self.message}>'
