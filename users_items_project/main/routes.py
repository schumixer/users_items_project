from flask import render_template, request, Blueprint,jsonify

main = Blueprint('main', __name__)


@main.route("/")
def home():
    response = {
        "description": f"Please visit {request.base_url}documented_api/doc for the documentation"
    }
    return jsonify(response)