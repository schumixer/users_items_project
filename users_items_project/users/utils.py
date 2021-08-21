from users_items_project.models import Users

def is_valid_login(login):
    user = Users.query.filter_by(login=login).first()
    if user:
        return False
    return True