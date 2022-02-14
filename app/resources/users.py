from app.database.model import db, User
from flask_restful import Resource, abort, fields, marshal_with, reqparse


def non_empty_string(s):
    s = s.strip()
    if not s:
        raise ValueError("Must not be empty string")
    return s


def check_boolean(s):
    s = s.lower()
    if s != 'true' and s != 'false':
        raise ValueError("Must be bool")
    return s


user_parser = reqparse.RequestParser()
user_parser.add_argument('username', required=True,
                         help='Username required', type=non_empty_string)
user_parser.add_argument('password', required=True,
                         help='Password required', type=non_empty_string)
user_parser.add_argument('admin', type=check_boolean)


def abort_if_username_already_exists(username):
    user = User.query.filter_by(username=username).first()
    if user:
        abort(409, message="A user with that username already exists.")


user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'admin': fields.Boolean
}


class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        args = user_parser.parse_args()
        username = args['username']
        abort_if_username_already_exists(username)
        isAdmin = False
        if args['admin'] is not None and args['admin'] == "true":
            isAdmin = True
        user = User(username=username, admin=isAdmin)
        user.hash_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201
