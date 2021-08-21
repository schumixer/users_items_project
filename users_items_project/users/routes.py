from flask import render_template, url_for, flash, redirect, request, Blueprint, jsonify, abort
from flask_login import login_user, current_user, logout_user, login_required
from users_items_project import db
from users_items_project.models import Users
from users_items_project.users.utils import is_valid_login


users = Blueprint('users', __name__)


@users.route("/registration", methods=['POST'])
def register():
    print(request.json)
    if not request.json:
        abort(400)
    login = request.json.get("login")
    if is_valid_login(login):
        password = request.json.get("password")
        user = Users(login=login,  password=password)
        db.session.add(user)
        db.session.commit()
        response = {
            "description": "The user was created"
        }
        return jsonify(response), 201
    abort(401)
    
    
@users.route("/login", methods=['POST'])
def login():
    # if current_user.is_authenticated:
    #     abort(401)
    print(request.json)
    if not request.json:
        abort(400)
    user = Users.query.filter_by(login=request.json.get("login")).first()
    if user and user.password == request.json.get("password"):
        login_user(user)
        response = {
            "token": user.get_token()
        }
        return jsonify(response)
    abort(401)
        

