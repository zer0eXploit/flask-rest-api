import sqlite3
from flask_restful import Resource, reqparse
from models.user import User_Model


class User_Register(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        "username",
        type=str,
        required=True,
        help="This field cannot be empty!"
    )

    parser.add_argument(
        "password",
        type=str,
        required=True,
        help="This field cannot be empty!"
    )

    def post(self):
        user_info = User_Register.parser.parse_args()

        if User_Model.get_by_username(user_info["username"]):
            return {"message": "Username already exists."}, 400

        user = User_Model(**user_info)
        user.upsert_user()

        return {"message": "User created."}, 201
