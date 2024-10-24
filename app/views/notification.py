from flask import Blueprint
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import Notification
from app import db
notifications_bp = Blueprint('notifications', __name__)

@notifications_bp.route('/notifications')
@login_required
def notifications():
    # unread_notifications = current_user.notifications.filter_by(current_user.id, is_read=False).all()
    # unread_notifications = Notification.query.filter_by(
    #     user_id = current_user.id,
    #     is_read = False
    # ).all()
    notifications = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notification.html', notifications=notifications)



@notifications_bp.route('/view/<int:notification_id>')
@login_required
def view_notification(notification_id):
    # 获取通知
    notification = Notification.query.get_or_404(notification_id)

    # 检查是否是当前用户的通知
    if notification.user_id == current_user.id:
        # 标记为已读
        notification.is_read = True
        db.session.commit()
    else:
        flash('你无权查看此通知。')
        return redirect(url_for('notifications.notifications'))

    # 重定向到对应的帖子详细页面
    return redirect(url_for('post.post_detail', post_id=notification.post_id))


@notifications_bp.route('/notifications/delete/<int:notification_id>')
@login_required
def delete_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)

    # 确保该通知属于当前用户
    if notification.user_id != current_user.id:
        flash('你无权删除此通知。')
        return redirect(url_for('notifications.notifications'))

    db.session.delete(notification)
    db.session.commit()

    flash('通知已删除。')
    return redirect(url_for('notifications.notifications'))
