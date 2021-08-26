import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "fcde7450d4e5aac339c0162ff2d4c99b"
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


# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
#     'sqlite://'
    
# class ProductionConfig(Config):
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#     'sqlite:///' + os.path.join(basedir, 'data.db')
    
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'data-dev.db')
    
# config = {
#     'development': DevelopmentConfig,
#     'testing': TestingConfig,
#     'production': ProductionConfig,
#     'default': DevelopmentConfig
# }