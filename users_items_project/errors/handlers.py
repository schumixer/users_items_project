from flask import Blueprint, jsonify

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(401)
def error_401(error):
    response = {
        "description": "Wrong credintials"
    }
    return response, 401