from flask import render_template, Blueprint, request, redirect, url_for, flash
from flask_login import current_user, login_required, login_user, logout_user
from ..models import Comment, Post, Notification
from datetime import datetime
from app import db

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/comment/<int:post_id>', methods=['POST'])
def create_comment(post_id):
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    if not content:
        flash('评论不能为空')
        return redirect(url_for('comment.create_comment', post_id=post_id))
    comment = Comment(content=content, author=current_user, post=post)
    db.session.add(comment)
    db.session.commit()

    #为作者添加通知
    if post.author.id != current_user.id:
        notification = Notification(
            user_id = post.author.id,
            post_id = post_id,
            comment_id = comment.id,
            message = f'来自{current_user.username}对{post.title}的评论',
        )
        db.session.add(notification)
        db.session.commit()
    flash('评论成功')
    return redirect(url_for('post.post_detail', post_id=post_id))

@comment_bp.route('/delete_comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('post.post_detail', post_id=comment.post_id))
