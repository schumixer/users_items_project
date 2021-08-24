from flask import request
from flask_restx  import  Namespace, Resource, fields

list_of_users_info = []
#Registration
registration_namespace = Namespace("registration", description="Registration API")

registration_model = registration_namespace.model('registration', {
    'login': fields.String(
        required = True,
        description='User login',
        help = 'String containing latin letters, digits, ".", "_", minLength = 2, maxLength 20'
    ),
    'password': fields.String(
        required = True,
        description='User password',
        help = 'String containing with minLength = 4, maxLength 15'
    )
})


@registration_namespace.route("")
class RegistrationClass(Resource):
    @registration_namespace.response(200, 'The user with such a login already exists. Please choose another login')
    @registration_namespace.response(201, 'The user was created')
    @registration_namespace.response(400, 'Wrong input')
    @registration_namespace.response(500, 'Internal Server error')
    @registration_namespace.expect(registration_model)
    def post(self):
        """Create a user with such a login and a password"""    
        
        try:
            login = request.json["login"]
            password = request.json["password"]
            for user in list_of_users_info:
                if login in user.values():
                    return "The user with such a login already exists. Please choose another login", 200
            list_of_users_info.append({
                "login" : login,
                "password": password
            })
        except KeyError as e:
            registration_namespace.abort(400, e.__doc__, status = "Wrong input", statusCode = "400")
        except Exception as e:
            registration_namespace.abort(500, e.__doc__, status = "Internal Server error", statusCode = "500")
        return {
			"description": "The user was created"
		}, 201
#Login
login_namespace = Namespace("login", description="Login API")

login_model = login_namespace.model('login', {
    'login': fields.String(
        required = True,
        description='User login',
        help = 'String containing latin letters, digits, ".", "_", minLength = 2, maxLength 20'
    ),
    'password': fields.String(
        required = True,
        description='User password',
        help = 'String containing with minLength = 4, maxLength 15'
    )
})


@login_namespace.route("")
class loginClass(Resource):
    @login_namespace.response(200, 'OK')
    @login_namespace.response(400, 'Wrong input')
    @login_namespace.response(401, 'Wrong credintials')
    @login_namespace.response(500, 'Internal Server error')
    @login_namespace.expect(login_model)
    def post(self):
        """Login a user with such a login and a password"""    
        
        try:
            login = request.json["login"]
            password = request.json["password"]
            is_valid_credentials = False
            for user in list_of_users_info:
                if user["login"] == login and user["password"] == password:
                    is_valid_credentials = True
                    break
            if not is_valid_credentials:
                return "Wrong credintials", 401
            
        except KeyError as e:
            login_namespace.abort(400, e.__doc__, status = "Wrong input", statusCode = "400")
        except Exception as e:
            login_namespace.abort(500, e.__doc__, status = "Internal Server error", statusCode = "500")
        return {
			"token": "token string"
		}, 200