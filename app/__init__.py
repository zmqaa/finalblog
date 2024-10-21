from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import click

#创建数据库实例和登录管理实例
db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    #从config.py中读取配置
    app.config.from_object('config.Config')

    #初始化数据库和管理系统
    db.init_app(app)
    login_manager.init_app(app)

    #在函数里面import延时导入避免循环import
    from app.models import User
    #必须
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    #注册初始化数据库命令
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='create after drop')
    def initdb(drop):
        if drop:
            db.drop_all()
        db.create_all()
        click.echo('数据库已初始化')

    #注册蓝图
    from app.views.auth import auth_bp
    from app.views.post import post_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(post_bp, url_prefix='/')

    return app