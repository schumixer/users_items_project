from flask import url_for, redirect, request, abort, Blueprint, jsonify
from flask_login import current_user
from flask_expects_json import expects_json
from users_items_project import db
from users_items_project.config import Config
from users_items_project.models import Items, Users

items = Blueprint("items", __name__)


@items.route("/items/new", methods=["POST"])
@expects_json(Config.item_creation_schema)
def new_item():
    user = Users.get_user_with_token(request.json.get("token"))
    if user:
        item = Items(name=request.json.get("name"), user_id=user.id)
        db.session.add(item)
        db.session.commit()
        response = {
            "id": item.id,
            "name": item.name,
            "description": "The item was created",
        }
        return jsonify(response), 201
    abort(401)


@items.route("/items/<int:id>", methods=["DELETE"])
@expects_json(Config.item_deletion_schema)
def delete_item(id):
    user = Users.get_user_with_token(request.json.get("token"))
    if user:
        item = Items.query.get_or_404(id, "The item was not found")
        if item.user_id != user.id:
            abort(403)
        db.session.delete(item)
        db.session.commit()

        response = {"description": "The item was deleted"}
        return jsonify(response), 200

    abort(401)


@items.route("/items", methods=["GET"])
def get_items():
    token = request.args.get("token")
    if token:
        user = Users.get_user_with_token(token)
        if user:
            items = Items.query.filter_by(author=user)
            response = []
            for item in items:
                response.append(item.to_json())
            return jsonify(response)
        else:
            abort(401)
    else:
        response = {
            "description": "Wrong input"
        }
        return jsonify(response), 400

