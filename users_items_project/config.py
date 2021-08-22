class Config:
    SECRET_KEY = "fcde7450d4e5aac339c0162ff2d4c99b"
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    registration_schema = {
        'type': 'object',
        'properties': {
            'login': {'type': 'string',  "minLength": 2, "maxLength": 20, "pattern": "^[\w.-]+$"},
            'password': {'type': 'string', "minLength": 4, "maxLength": 15}
        },
        'required': ['login', 'password']
    }
    item_creation_schema = {
        'type': 'object',
        'properties': {
            'token': {'type': 'string',  "minLength": 1, "maxLength": 1000},
            'name': {'type': 'string', "minLength": 2, "maxLength": 50}
        },
        'required': ['token', 'name']
    }
    item_deletion_schema ={
        'type': 'object',
        'properties': {
            'token': {'type': 'string',  "minLength": 1, "maxLength": 1000}
        },
        'required': ['token']
    }
    item_move_schema ={
        'type': 'object',
        'properties': {
            'id': {'type': ['string', 'number']},
            'login': {'type': 'string',  "minLength": 2, "maxLength": 20, "pattern": "^[\w.-]+$"},
            'token': {'type': 'string',  "minLength": 1, "maxLength": 1000}
        },
        'required': ['id','login', 'token']
    }
