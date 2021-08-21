from flask import  redirect, request, Blueprint, jsonify, abort
from sqlalchemy.orm import load_only
from users_items_project import db
from users_items_project.models import Users, Items
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
    
