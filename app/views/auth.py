from flask import redirect, url_for, render_template, Blueprint, request, flash, current_app
from flask_login import current_user, login_user, login_required, logout_user
from ..models import User, Post
from app import db
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
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
            return redirect(url_for('auth.login'))

        user = User.query.filter_by(username=username).first()
        if user is not None:
            if username == user.username and user.check_password(password):
                login_user(user)
                flash('登录成功！')
                return redirect(url_for('post.index'))
        else:
            flash('用户名不存在')
            return redirect(url_for('auth.login'))
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        email = request.form['email']

        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash('用户名或邮箱已被使用')
            return redirect(url_for('auth.register'))

        if password2 != password:
            flash('密码不一致')
            return redirect(url_for('auth.register'))

        user = User(username=username, email=email)
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
@login_required
def profile():
    if current_user.is_authenticated:
        user = current_user
        user_posts = Post.query.filter_by(author_id=user.id).all()
        return render_template('profile.html', posts=user_posts, user=user)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_extension = filename.rsplit('.', 1)[1].lower()
        new_filename = f'{uuid.uuid4()}.{file_extension}'
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename)
        file.save(filepath)
        return new_filename
    return None

@auth_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    if request.method == 'POST':

        new_username = request.form.get('username')
        new_avatar = request.files.get('avatar')
        new_email = request.form.get('email')

        if new_username:
            user.username = new_username

        if new_email:
            user.email = new_email

        if new_avatar and allowed_file(new_avatar.filename):
            filename = secure_filename(new_avatar.filename)
            avatar_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            new_avatar.save(avatar_path)
            user.avatar = filename
        # if new_avatar and allowed_file(new_avatar.filename):
        #     filename = save_file(new_avatar)
        #     if filename:
        #         user.avatar = filename
        #         flash('头像更改完成')
        #     else:
        #         flash('上传失败')

        db.session.commit()
        flash('更改成功！')
        return redirect(url_for('auth.profile'))

    return render_template('edit_profile.html')

