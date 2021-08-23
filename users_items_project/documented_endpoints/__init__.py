from flask import Blueprint
from flask_restx import  Api

from users_items_project.documented_endpoints.registration_login import (
    login_namespace, registration_namespace
)

documented_endpoint = Blueprint(
    "documented_api", __name__, url_prefix="/documented_api"
)

api_extension = Api(
    documented_endpoint,
    title='Flask users and items project',
    version='1.0',
    description='Documentation for users and items project',
    doc='/doc'
)

api_extension.add_namespace(registration_namespace)
api_extension.add_namespace(login_namespace)
