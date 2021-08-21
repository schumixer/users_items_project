from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, jsonify)
from flask_login import current_user
from users_items_project import db
from users_items_project.models import Items, Users

items = Blueprint('items', __name__)


@items.route("/items/new", methods=['POST'])
def new_item():
    print(request.json)
    if not request.json:
        abort(400)
    user = Users.get_user_with_token(request.json.get("token"))
    if user:
        item = Items(name = request.json.get("name"), user_id = user.id)
        db.session.add(item)
        db.session.commit()
        response = {
            "id": item.id,
            "name": item.name,
            "description": "The item was created"
        }
        return jsonify(response)
    abort(401)
    
@items.route("/items/<int:id>", methods=['DELETE'])
def delete_item(id):
    print(request.json)
    if not request.json:
        abort(400)
        
    user = Users.get_user_with_token(request.json.get("token"))
    if user:
        item = Items.query.get_or_404(id)
        
        if item.user != user:
            abort(403)
        db.session.delete(item)
        db.session.commit()
        
        response = {
            "description": "The item was deleted"
        }
        return jsonify(response)
       
    abort(401)
    
    
@items.route("/items", methods=['GET'])
def get_items():
    print(request.json)
    if not request.json:
        abort(400)
        
    user = Users.get_user_with_token(request.json.get("token"))
    if user:
        
        items =  Items.query.filter_by(author=user)
        response = []
        for item in items:
            response.append(item.to_json())
        print(response)
        return jsonify(response)
       
    abort(401)
    
    


