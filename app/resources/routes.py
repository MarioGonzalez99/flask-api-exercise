from app.resources.users import Users
from app.resources.login import Login
from flask_restful import Api

api = Api()


def initialize_routes(api):
    api.add_resource(Users, '/v1/users')
    api.add_resource(Login, '/v1/login')
