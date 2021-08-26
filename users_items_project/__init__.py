from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from users_items_project.config import DevelopmentConfig

# def create_app(config_class):
app = Flask(__name__)

app.config.from_object(DevelopmentConfig)

db = SQLAlchemy(app)

from users_items_project.users.routes import users
from users_items_project.main.routes import main
from users_items_project.items.routes import items
from users_items_project.errors.handlers import errors
from users_items_project.documented_endpoints import documented_endpoint
    
app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(items)
app.register_blueprint(errors)
app.register_blueprint(documented_endpoint)
    # return app