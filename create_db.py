from users_items_project import db
from users_items_project.models import Users, Items
db.drop_all()
db.create_all()