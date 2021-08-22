
from users_items_project.models import Users


def is_new_login(login):
    user = Users.query.filter_by(login=login).first()
    if user:
        return False
    return True

# def is_valid_json(json, *args):
#     if not json:
#         return False
#     if sorted(list(json.keys())) != sorted(args):
#         return False
    
#     return True
        
# def is_valid_login(login):
    
    
#     return True
    