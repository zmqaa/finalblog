from flask_restful import Resource, reqparse
from app.models import User
from app import db
from flask import jsonify

# 用户的请求解析器
user_parser = reqparse.RequestParser()
user_parser.add_argument("username", type=str, required=True, help="Username is required")
user_parser.add_argument("password", type=str, required=True, help="Password is required")
user_parser.add_argument("email", type=str, required=True, help="Email is required")

class UserListResource(Resource):
    def get(self):
        """获取所有用户"""
        users = User.query.all()
        return jsonify([{
            "id": user.id,
            "username": user.username,
            "email": user.email
        } for user in users])

    def post(self):
        """创建新用户"""
        args = user_parser.parse_args()
        user = User(username=args['username'], email=args['email'])
        user.set_password(args['password'])  # 加密密码
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": "User created",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 201

class UserResource(Resource):
    def get(self, user_id):
        """获取指定ID的用户"""
        user = User.query.get_or_404(user_id)
        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })
