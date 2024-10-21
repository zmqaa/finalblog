from flask import render_template, Blueprint, request, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from ..models import Comment, Post
from datetime import datetime

comment_bp = Blueprint('comment', __name__)