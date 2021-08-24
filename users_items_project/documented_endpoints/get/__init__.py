from flask import request
from flask_restx  import  Namespace, Resource, fields,reqparse, inputs

get_namespace = Namespace("get", description="get API")



token_to_expect = "token"
get_model_expect_post = get_namespace.model('get', 
    {
        'token': fields.String(
            description='User token',
            default= token_to_expect
        ),
        'name': fields.String(
            description='Item name'
        )
    }
)



get_model_expect = reqparse.RequestParser()
get_model_expect.add_argument('data',
                    help="data",
                    default="data", required=True)
get_model_expect.add_argument('token',
                    help="token",
                    default="token", required=True)

@get_namespace.route("")
class getClass(Resource):
    @get_namespace.response(200, 'OK')
    @get_namespace.response(400, 'Wrong input')
    @get_namespace.response(401, 'Wrong credintials')
    @get_namespace.response(403, "You have no access to this resourse. Wrong login")
    @get_namespace.response(404,"The user that had the item doesn't exist or the user doesn't have this item")
    @get_namespace.response(500, 'Internal Server error')
    @get_namespace.expect(get_model_expect)
    def get(self):
        """Move the item"""    
        
        try:
            token = request.args["token"]
            data = request.args["data"]
            if token == token_to_expect:
                return {"description": "The item was moved"}, 200
            else:
                return {
                    "description": "Wrong credintials"
                }, 401
        except KeyError as e:
            get_namespace.abort(400, e.__doc__, status = "Wrong input", statusCode = "400")
        except Exception as e:
            get_namespace.abort(500, e.__doc__, status = "Internal Server error", statusCode = "500")
            
            
