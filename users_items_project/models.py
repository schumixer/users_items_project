from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
from users_items_project import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    items = db.relationship("Items", backref="author", lazy=True)

    def get_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")
    
    @staticmethod
    def get_link(user_login_to, item_id, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        token = s.dumps({"user_login_to": user_login_to, "item_id": item_id}).decode("utf-8")
        link = url_for("users.get", token=token, _external=True)
        return link

    @staticmethod
    def get_user_with_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return Users.query.get(user_id)
    
    @staticmethod
    def get_data_from_link(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            data = s.loads(token)
        except:
            return None
        return data

    def __repr__(self):
        return f"Users('{self.username}')"


class Items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.name}')"

    def to_json(self):
        return {"id": self.id, "name": self.name}
