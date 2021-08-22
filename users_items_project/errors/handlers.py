from flask import Blueprint, jsonify

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(401)
def error_401(error):
    response = {
        "description": "Wrong credintials"
    }
    return jsonify(response), 401

@errors.app_errorhandler(404)
def error_404(error):
    response = {
        "description": str(error)
    }
    return jsonify(response), 404

@errors.app_errorhandler(403)
def error_403(error):
    response = {
        "description": str(error)
    }
    return jsonify(response), 403