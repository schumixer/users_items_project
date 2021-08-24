from flask import request
from flask_restx  import  Namespace, Resource, fields,reqparse, inputs

items_namespace = Namespace("items", description="Items API")

list_of_items = [
            {
                "id": 1,
                "name": "banana"
		    },
            {
                "id": 2,
                "name": "apple"
		    },
            {
                "id": 3,
                "name": "orange"
		    },
            {
                 "id": 4,
                 "name": "lemon"
            }
]

token_to_expect = "token"
id_to_expect = len(list_of_items)
items_model_expect_post = items_namespace.model('items', 
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

items_model_expect_delete = items_namespace.model('items', 
    {
        'token': fields.String(
            description='User token',
            default= token_to_expect
        )
    }
)

items_model_expect_get = reqparse.RequestParser()
items_model_expect_get.add_argument('token',
                    help="token",
                    default="token", required=True)


@items_namespace.route("")
class itemsClass(Resource):
    @items_namespace.response(200, 'OK')
    @items_namespace.response(400, 'Wrong input')
    @items_namespace.response(401, 'Wrong credintials')
    @items_namespace.response(500, 'Internal Server error')
    @items_namespace.expect(items_model_expect_get)
    def get(self):
        """Get the list of objects"""    
        
        try:
            token = request.args["token"]
            if token == token_to_expect:
                return list_of_items, 200
            else:
                return {
                    "description": "Wrong credintials"
                }, 401
        except KeyError as e:
            items_namespace.abort(400, e.__doc__, status = "Wrong input", statusCode = "400")
        except Exception as e:
            items_namespace.abort(500, e.__doc__, status = "Internal Server error", statusCode = "500")
            
            
@items_namespace.route("/new")
class itemsClass(Resource):
    @items_namespace.response(201, 'The item was created')
    @items_namespace.response(400, 'Wrong input')
    @items_namespace.response(401, 'Wrong credintials')
    @items_namespace.response(500, 'Internal Server error')
    @items_namespace.expect(items_model_expect_post)
    def post(self):
        """Creation of a new object"""    
        global id_to_expect
        try:
            token = request.json["token"]
            name = request.json["name"]
            if token != token_to_expect:
                return "Wrong credintials", 401
            list_of_items.append(
                {
                    "id": id_to_expect,
                    "name": name
                }
            )
            
            response = {
                "id": id_to_expect,
                "name": name,
                "description": "The item was created",
            }
            id_to_expect+=1
            return response, 201
        except KeyError as e:
            items_namespace.abort(400, e.__doc__, status = "Wrong input", statusCode = "400")
        except Exception as e:
            items_namespace.abort(500, e.__doc__, status = "Internal Server error", statusCode = "500")

def find_item_by(id, list_of_items):
    for i in range(len(list_of_items)):
        if list_of_items[i].get("id") == id:
            return i
    return None
    

@items_namespace.route("/<int:id>")
class itemsClass(Resource):
    @items_namespace.response(200, 'The item was deleted')
    @items_namespace.response(400, 'Wrong input')
    @items_namespace.response(401, 'Wrong credintials')
    @items_namespace.response(403, 'The access is forbidden')
    @items_namespace.response(404, 'The item was not found')
    @items_namespace.response(500, 'Internal Server error')
    @items_namespace.expect(items_model_expect_delete)
    def delete(self, id):
        """Delete the object with id"""    
        
        global id_to_expect
        try:
            token = request.json["token"]
            if token == token_to_expect:
                item_index = find_item_by(id, list_of_items)
                if item_index:
                    del list_of_items[item_index]
                    response = {"description": "The item was deleted"}
                    id_to_expect-=1
                    return response, 200
                else:
                    response = {"description": "The item was not found"}
                    return response, 404
            else:
                return {
                    "description": "Wrong credintials"
                }, 401
        except KeyError as e:
            items_namespace.abort(400, e.__doc__, status = "Wrong input", statusCode = "400")
        except Exception as e:
            items_namespace.abort(500, e.__doc__, status = "Internal Server error", statusCode = "500")