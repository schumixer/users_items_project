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
@expects_json(Config.item_move_schema)
def send():
    user_from = Users.get_user_with_token(request.json.get("token"))
    if user_from:
        user_to =  Users.query.filter_by(login = request.json.get("login")).first()
        if user_to:
            selected_item =  Items.query.filter_by(author=user_from, id = int(request.json.get("id"))).first()
            if selected_item:
                response = {
                    "link": Users.get_link(user_from_id=user_from.id,
                                           user_to_id=user_to.id, 
                                           item_id=selected_item.id)
                }    
                return jsonify(response)
            else:
                abort(404, "The item was not found")
        else:
            abort(404, "The user was not found")
    else:
        abort(401)


@users.route("/get", methods=['GET'])
def get():
    user_to = Users.get_user_with_token(request.args.get("token"))
    if user_to:
        data = Users.get_data_from_link(request.args.get("data"))
        if data:
            user_from_id_link = data["user_from_id"]
            user_to_id_link = data["user_to_id"]
            item_id_link = data["item_id"]
            if Items.query.filter_by(user_id = user_from_id_link, id = int(item_id_link)).first():
                if user_to.id == user_to_id_link:
                    Items.query.get(item_id_link).user_id = user_to.id
                    db.session.commit()
                    response = {
                        "description": "The item was moved"
                    }
                    return jsonify(response), 200
                else:
                    abort(403, "You have no access to this resourse. Wrong login")
            else:
                abort(404, "The user that had the item doesn't exist or the user doesn't have this item")
        else:
            abort(401)
    else:
        abort(401)
    
