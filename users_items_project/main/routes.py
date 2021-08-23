from flask import render_template, request, Blueprint,jsonify

main = Blueprint('main', __name__)


# @main.route("/")
# def home():
#     response = {
#         "description": "Welcome!"
#     }
#     return jsonify(response)