from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.token_blacklist import BlacklistToken


class TokenList(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        tokens = BlacklistToken.get_all_tokens_by_user_id(user_id)

        if tokens:
            return {
                'tokens': [t.json() for t in tokens]
            }

        return {
            'tokens': []
        }
