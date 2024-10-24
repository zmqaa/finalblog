from flask import Flask, Blueprint
from flask_restful import Api
from .post_resources import PostListResource, PostResource
from .user_resources import UserListResource, UserResource
from .comment_resources import CommentListResource
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(PostListResource, '/posts')
api.add_resource(PostResource, '/post/<int:post_id>')

