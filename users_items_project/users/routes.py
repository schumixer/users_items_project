from flask import  redirect, request, Blueprint, jsonify, abort
from flask_expects_json import expects_json
from users_items_project import db
from users_items_project.models import Users, Items
from users_items_project.users.utils import is_new_login
from users_items_project.config import Config

users = Blueprint('users', __name__)


@users.route("/registration", methods=['POST'])
@expects_json(Config.registration_schema)
def register():
    login = request.json.get("login")
    if is_new_login(login):
        user = Users(login=login,  password=request.json.get("password"))
        db.session.add(user)
        db.session.commit()
        response = {
            "description": "The user was created"
        }
        return jsonify(response), 201
    response = {
            "description": "The user with such a login already exists. Please choose another login"
        }
    return jsonify(response), 200
    
    
@users.route("/login", methods=['POST'])
@expects_json(Config.registration_schema)
def login():
    user = Users.query.filter_by(login=request.json.get("login")).first()
    if user and user.password == request.json.get("password"):
        response = {
            "token": user.get_token()
        }
        return jsonify(response)
    abort(401)
    
        
@users.route("/send", methods=['POST'])
def send():
    print(request.json)
    if not request.json:
        abort(400)
    user_from = Users.get_user_with_token(request.json.get("token"))
    if user_from:
        user_to =  Users.query.filter_by(login = request.json.get("login")).first()
        if user_to:
            selected_item =  Items.query.filter_by(author=user_from, id = int(request.json.get("id"))).first()
            if selected_item:
            
                response = {
                    "link": Users.get_link(user_login_to=user_to.login, item_id=selected_item.id)
                }    
                    
                return jsonify(response)
    abort(401)


@users.route("/get/<token>", methods=['GET'])
def get(token):
    print(request.json)
    if not request.json:
        abort(400)
    user = Users.get_user_with_token(request.json.get("token"))
    if user:
        data = Users.get_data_from_link(token)
        user_from_login = data["user_login_to"]
        item_id = data["item_id"]
        # user_login = Items.query.get(item_id).author.login
        if user.login == user_from_login:
            Items.query.get(item_id).user_id = Users.query.filter_by(login = user_from_login).first().id
            db.session.commit()
            response = {
                "description": "The item was moved"
            }
            return jsonify(response), 201
    abort(401)
    
