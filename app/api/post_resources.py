from flask_restful import Resource, reqparse, abort
from app.models import Post, User
from app import db
from flask import jsonify

# 请求解析器，用于处理文章的POST和PUT请求参数
post_parser = reqparse.RequestParser()
post_parser.add_argument("title", type=str, required=True, help="Title is required")
post_parser.add_argument("content", type=str, required=True, help="Content is required")
post_parser.add_argument("author_id", type=int, required=True, help="Author ID is required")


class PostListResource(Resource):
    def get(self):
        """获取所有文章"""
        posts = Post.query.all()
        return jsonify([{
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": post.author.username,
            "create_time": post.create_time.isoformat()
        } for post in posts])

    def post(self):
        """创建新文章"""
        args = post_parser.parse_args()
        user = User.query.get(args['author_id'])  # 确保作者ID有效
        if not user:
            abort(404, message="User not found")

        new_post = Post(
            title=args['title'],
            content=args['content'],
            author_id=args['author_id']
        )
        db.session.add(new_post)
        db.session.commit()
        return jsonify({
            "message": "Post created",
            "post": {
                "id": new_post.id,
                "title": new_post.title,
                "content": new_post.content,
                "author": new_post.author.username
            }
        }), 201


class PostResource(Resource):
    def get(self, post_id):
        """获取特定ID的文章"""
        post = Post.query.get_or_404(post_id)
        return jsonify({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author": post.author.username,
            "create_time": post.create_time.isoformat()
        })

    def put(self, post_id):
        """更新特定ID的文章"""
        post = Post.query.get_or_404(post_id)
        args = post_parser.parse_args()

        # 更新文章内容
        post.title = args['title']
        post.content = args['content']
        db.session.commit()
        return jsonify({
            "message": "Post updated",
            "post": {
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "author": post.author.username
            }
        })

    def delete(self, post_id):
        """删除特定ID的文章"""
        post = Post.query.get_or_404(post_id)
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post deleted"})
