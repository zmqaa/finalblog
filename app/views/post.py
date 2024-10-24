from flask import render_template, Blueprint, request, redirect, url_for, flash
from ..models import Post, Comment
from app import db
from flask_login import current_user, login_required
import math

post_bp = Blueprint('post', __name__)

@post_bp.route('/')
def index():
    post_count = Post.query.count()
    #获取页码
    page = request.args.get('page', 1, type=int)
    per_page = 5
    al_page = math.ceil(post_count / per_page)
    posts = Post.query.order_by(Post.create_time.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    return render_template('index.html', posts=posts, len=post_count, al_page=al_page)

@post_bp.route('/post/<int:post_id>')
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    page=request.args.get('page', 1, type=int)
    per_page = 5
    comment_count = post.comments.count()
    comments = post.comments.order_by(Comment.comment_time.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    return render_template('post_detail.html', post=post, comments=comments, len=comment_count)

@post_bp.route('/create_post', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author == current_user:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('auth.profile'))

@post_bp.route('/search_post')
def search_post():
    query = request.args.get('q', '').strip()  #strip去除空格
    if query:
        results = Post.query.filter(
            db.or_(
                Post.title.like(f'%{query}%'),   #两边都有%在任何地方出现都可以
                Post.content.like(f'%{query}%')  #ilike就是不区分大小写
            )
        ).all()
    else:
        results = []
    return render_template('search.html', query=query, results=results)
