from flask import Blueprint
from flask_restful import Api


from api.login_api import LoginAPI

api_routes = Blueprint('api_routes', __name__)
routes_api = Api(api_routes)
routes_api.add_resource(LoginAPI, '/login/<string:username>/<string:password>')