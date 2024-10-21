from flask import redirect, url_for, render_template, Blueprint, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from ..models import User, Post
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('post.index'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('无效输入')
            return redirect(url_for('login'))

        user = User.query.filter_by(username=username).first()
        if username == user.username and user.check_password(password):
            login_user(user)
            flash('登录成功！')
            return redirect(url_for('post.index'))
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        if User.query.filter_by(username=username).first():
            flash('用户名已被使用')
            return redirect(url_for('auth.register'))
        if password2 != password:
            flash('密码不一致')
            return redirect(url_for('auth.register'))
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('注册成功')
            return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('再见')
    return redirect(url_for('post.index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    user = current_user
    user_posts = Post.query.filter_by(author_id=user.id).all()
    return render_template('profile.html', posts=user_posts, user=user)