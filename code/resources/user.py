from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.user import UserModel


class User(Resource):
    @classmethod
    @jwt_required()
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {
                'error': 'User not found.'
            }, 404
        return user.json()

    @classmethod
    @jwt_required()
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {
                'error': 'User not found.'
            }, 404

        user.delete_from_db()
        return {
            'message': 'User deleted.'
        }


class UserList(Resource):
    @classmethod
    @jwt_required()
    def get(cls):
        return {'users': list(map(lambda user: user.json(), UserModel.get_all()))}


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="Please enter a username."
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Please enter a password."
    )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {
                'error': 'User {} already exists!'.format(data['username'])
            }, 400

        new_user = UserModel(**data)
        new_user.save_to_db()

        return {'message': 'User created successfully.'}, 201
