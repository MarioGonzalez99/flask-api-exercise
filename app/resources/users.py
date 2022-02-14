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
user_parser.add_argument('Authorization', location='headers',
                         required=True, help='Authorization token required')


def abort_if_username_already_exists(username):
    user = User.query.filter_by(username=username).first()
    if user:
        abort(409, message="A user with that username already exists.")


def abort_if_creator_not_admin(bearer_token):
    token_res = bearer_token.split()
    if len(token_res) < 2:
        abort(
            400, message='Please, provide a valid bearer token in Authorization header. Ex: Bearer [token]')
    token = token_res[1]
    user_id = User.decode_auth_token(token)
    try:
        user_id = int(user_id)
    except:
        abort(401, message=user_id)

    user = User.query.filter_by(id=user_id).first()
    if user is None or user.admin == False:
        abort(401, message='Not authorized to use this function')


def check_if_admin(isAdmin):
    return True if isAdmin is not None and isAdmin == "true" else False


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
        abort_if_creator_not_admin(args['Authorization'])
        username = args['username']
        abort_if_username_already_exists(username)
        isAdmin = check_if_admin(args['admin'])
        user = User(username=username, admin=isAdmin)
        user.hash_password(args['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201
