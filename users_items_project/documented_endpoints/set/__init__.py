from flask import request
from flask_restx  import  Namespace, Resource, fields,reqparse, inputs

set_namespace = Namespace("set", description="set API")

token_to_expect = "token"

link_to_expect = "link"

id_to_expect = 1

set_model_expect = set_namespace.model('set', 
    {
        "id": fields.Integer(
            description='Item ID',
            default= id_to_expect
        ),
        'token': fields.String(
            description='User token',
            default= token_to_expect
        ),
        'login': fields.String(
            description='Login of the user taking the item'
        )
    }
)

@set_namespace.route("")
class setClass(Resource):
    @set_namespace.response(200, 'OK')
    @set_namespace.response(400, 'Wrong input')
    @set_namespace.response(401, 'Wrong credintials')
    @set_namespace.response(404, 'The item or user was not found')
    @set_namespace.response(500, 'Internal Server error')
    @set_namespace.expect(set_model_expect)
    def post(self):
        """Generation of the link"""    
        
        try:
            id = request.json["id"]
            token = request.json["token"]
            login = request.json["login"]
            if token != token_to_expect:
                return {
                    "link": "Wrong credintials"
                }, 401
            else:
                return  {"link": link_to_expect}
        except KeyError as e:
            set_namespace.abort(400, e.__doc__, status = "Wrong input", statusCode = "400")
        except Exception as e:
            set_namespace.abort(500, e.__doc__, status = "Internal Server error", statusCode = "500")
