from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
from users_items_project.config import Config

config_class=Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


from users_items_project.users.routes import users
from users_items_project.main.routes import main
app.register_blueprint(users)
app.register_blueprint(main)

