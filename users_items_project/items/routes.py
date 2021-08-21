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
    
    
    
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')

