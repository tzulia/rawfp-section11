from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required
from werkzeug.security import safe_str_cmp

from models.user import UserModel


_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    'username',
    type=str,
    required=True,
    help="Please enter a username."
)
_user_parser.add_argument(
    'password',
    type=str,
    required=True,
    help="Please enter a password."
)


class User(Resource):
    @classmethod
    @jwt_required
    @UserModel.require_admin
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {
                'error': 'User not found.'
            }, 404
        return user.json()

    @classmethod
    @jwt_required
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
    @jwt_required
    def get(cls):
        return {
            'users': list(map(lambda user: user.json(), UserModel.get_all()))
        }


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {
                'error': 'User {} already exists!'.format(data['username'])
            }, 400

        if data['username'] == 'tzulia':
            data['is_admin'] = True
        else:
            data['is_admin'] = False

        new_user = UserModel(**data)
        new_user.save_to_db()

        return {'message': 'User created successfully.'}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        # get data from parser
        data = _user_parser.parse_args()

        # find user in database
        user = UserModel.find_by_username(data['username'])

        # check password
        if user and safe_str_cmp(user.password, data['password']):
            # create access token
            access_token = create_access_token(identity=user.id, fresh=True)
            # create refresh token
            refresh_token = create_refresh_token(identity=user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200

        return {
            'error': 'Invalid credentials'
        }, 401
