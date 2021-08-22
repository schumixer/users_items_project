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
