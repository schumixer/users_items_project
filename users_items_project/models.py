from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, url_for
from users_items_project import db
from flask_login import UserMixin

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    items = db.relationship("Items", backref="author", lazy=True)

    def get_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")
    
    @staticmethod
    def get_link(user_from_id,  item_id, user_to_id, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        token = s.dumps({"user_from_id": user_from_id,
                         "item_id": item_id,
                         "user_to_id": user_to_id,
                         }).decode("utf-8")
        link = url_for("users.get", data=token, _external=True)
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
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"Post('{self.name}')"

    def to_json(self):
        return {"id": self.id, "name": self.name}
