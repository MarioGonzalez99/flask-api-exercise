from app.database.model import User
from flask_restful import Resource, abort, reqparse

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', required=True, help='Username required')
login_parser.add_argument('password', required=True, help='Password required')


def abort_if_invalid_authentication():
    abort(401, message="Invalid credentials")


class Login(Resource):

    def post(self):
        args = login_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if user and user.verify_password(args['password']):
            token = user.encode_auth_token(user.id)
            return {'token': token}, 201

        abort_if_invalid_authentication()
