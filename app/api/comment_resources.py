from flask_restful import Resource, reqparse, abort
from app.models import Comment, Post, User
from app import db
from flask import jsonify

# 评论请求解析器
comment_parser = reqparse.RequestParser()
comment_parser.add_argument("content", type=str, required=True, help="Content is required")
comment_parser.add_argument("post_id", type=int, required=True, help="Post ID is required")
comment_parser.add_argument("author_id", type=int, required=True, help="Author ID is required")


class CommentListResource(Resource):
    def get(self):
        """获取所有评论"""
        comments = Comment.query.all()
        return jsonify([{
            "id": comment.id,
            "content": comment.content,
            "post_id": comment.post_id,
            "author": comment.author.username,
            "comment_time": comment.comment_time.isoformat()
        } for comment in comments])

    def post(self):
        """创建新评论"""
        args = comment_parser.parse_args()

        # 检查文章和作者是否存在
        post = Post.query.get(args['post_id'])
        author = User.query.get(args['author_id'])
        if not post or not author:
            abort(404, message="Post or User not found")

        new_comment = Comment(
            content=args['content'],
            post_id=args['post_id'],
            author_id=args['author_id']
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({
            "message": "Comment created",
            "comment": {
                "id": new_comment.id,
                "content": new_comment.content,
                "post_id": new_comment.post_id,
                "author": new_comment.author.username
            }
        }), 201
