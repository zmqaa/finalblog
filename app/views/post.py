from flask import render_template, Blueprint, request, redirect, url_for, flash
from ..models import Post
from app import db
from flask_login import current_user


post_bp = Blueprint('post', __name__)

@post_bp.route('/')
def index():
    posts = Post.query.order_by(Post.create_time.desc()).all()
    return render_template('index.html', posts=posts)

@post_bp.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_detail.html', post=post)

@post_bp.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('发布成功!')
        return redirect(url_for('post.index'))

    return render_template('create_post.html')

@post_bp.route('/edit_post/<int:post_id>', methods=["GET", "POST"])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id) #获取post对象

    if  post.author == current_user:
        if request.method == 'POST':
            post.title = request.form['title']
            post.content = request.form['content']
            db.session.commit()
            flash('修改完成！')
            return redirect(url_for('auth.profile'))
    return render_template('edit_post.html', post=post)

@post_bp.route('delete_post/<int:post_id>', methods=["GET", "POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('auth.profile'))
