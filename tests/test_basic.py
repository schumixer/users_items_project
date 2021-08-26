# project/test_basic.py
import os
import unittest
from flask import request
from users_items_project import app, db
import urllib.parse as urlparse
from urllib.parse import parse_qs
TEST_DB = "test.db"


class BasicTests(unittest.TestCase):
    ############################
    #### setup and teardown ####
    ############################
    @classmethod
    def setUpClass(cls):
        basedir = os.path.dirname(os.path.abspath(__file__))
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
            basedir, TEST_DB
        )

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()
        db.create_all()

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # ###############
    # #### tests ####
    # ###############

    def test_main_page(self):
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_user_registration(self):
        response = self.register("Tom", "1234")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"description": "The user was created"})

    def test_invalid_user_registration(self):
        response = self.register("Tom", "1234")
        response = self.register("Tom", "12345")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json,
            {
                "description": "The user with such a login already exists. Please choose another login"
            },
        )

    def test_valid_user_authorization(self):
        _ = self.register("Tom", "1234")
        response_auth = self.login("Tom", "1234")
        self.assertEqual(response_auth.status_code, 200)

    def test_invalid_user_authorization(self):
        _ = self.register("Tom", "1234")
        response_auth = self.login("Tom", "12345")
        self.assertEqual(response_auth.status_code, 401)

    def test_valid_item_creation(self):
        _ = self.register("Tom", "1234")
        response_auth = self.login("Tom", "1234")
        response = self.create_item(response_auth.json["token"], "banana")
        response_to_wait = {
            "id": response.json["id"],
            "name": response.json["name"],
            "description": "The item was created",
        }
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, response_to_wait)

    def test_invalid_item_creation(self):
        _ = self.register("Tom", "1234")
        response_auth = self.login("Tom", "1234")
        response = self.create_item(
            response_auth.json["token"] + "wrong token", "banana"
        )
        self.assertEqual(response.status_code, 401)

    def test_valid_item_deletion(self):
        _ = self.register("Tom", "1234")
        response_auth = self.login("Tom", "1234")
        _ = self.create_item(response_auth.json["token"], "banana")
        _ = self.create_item(response_auth.json["token"], "milk")
        response_delete_1 = self.delete_item(response_auth.json["token"], 1)
        response_delete_2 = self.delete_item(response_auth.json["token"], 2)
        response_to_wait = {"description": "The item was deleted"}
        self.assertEqual(response_delete_1.status_code, 200)
        self.assertEqual(response_delete_1.json, response_to_wait)
        self.assertEqual(response_delete_2.status_code, 200)
        self.assertEqual(response_delete_2.json, response_to_wait)

    def test_invalid_item_deletion_401(self):
        _ = self.register("Tom", "1234")
        response_auth = self.login("Tom", "1234")
        _ = self.create_item(response_auth.json["token"], "banana")
        response_delete_1 = self.delete_item(
            response_auth.json["token"] + "wrong token", 1
        )
        self.assertEqual(response_delete_1.status_code, 401)

    def test_invalid_item_deletion_404(self):
        _ = self.register("Tom", "1234")
        response_auth = self.login("Tom", "1234")
        _ = self.create_item(response_auth.json["token"], "banana")
        response_delete_1 = self.delete_item(response_auth.json["token"], 2)
        self.assertEqual(response_delete_1.status_code, 404)

    def test_invalid_item_deletion_403(self):
        _ = self.register("Tom", "1234")
        response_auth_1 = self.login("Tom", "1234")
        _ = self.create_item(response_auth_1.json["token"], "banana")

        _ = self.register("Jack", "1234")
        response_auth_2 = self.login("Jack", "1234")
        _ = self.create_item(response_auth_2.json["token"], "milk")

        response_delete_1 = self.delete_item(response_auth_1.json["token"], 2)
        self.assertEqual(response_delete_1.status_code, 403)

    def test_valid_items_get(self):
        _ = self.register("Tom", "1234")
        response_auth = self.login("Tom", "1234")
        _ = self.create_item(response_auth.json["token"], "banana")
        _ = self.create_item(response_auth.json["token"], "milk")
        response_get = self.get_items(response_auth.json["token"])
        response_to_wait = [
            {"id": 1, "name": "banana"},
            {"id": 2, "name": "milk"},
        ]
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_get.json, response_to_wait)

    def test_invalid_items_get_401(self):
        _ = self.register("Tom", "1234")
        response_auth = self.login("Tom", "1234")
        _ = self.create_item(response_auth.json["token"], "banana")
        _ = self.create_item(response_auth.json["token"], "milk")
        response_get = self.get_items(response_auth.json["token"] + "wrong token")
        self.assertEqual(response_get.status_code, 401)

    def test_valid_send_item(self):
        _ = self.register("Tom", "1234")
        response_auth_1 = self.login("Tom", "1234")
        _ = self.create_item(response_auth_1.json["token"], "banana")
        _ = self.create_item(response_auth_1.json["token"], "milk")

        _ = self.register("Jack", "1234")
        _ = self.login("Jack", "1234")

        response_send = self.send_item(response_auth_1.json["token"], 1, "Jack")
        self.assertEqual(response_send.status_code, 200)

    def test_invalid_send_item(self):
        _ = self.register("Tom", "1234")
        response_auth_1 = self.login("Tom", "1234")
        _ = self.create_item(response_auth_1.json["token"], "banana")
        _ = self.create_item(response_auth_1.json["token"], "milk")

        _ = self.register("Jack", "1234")
        _ = self.login("Jack", "1234")

        response_send = self.send_item(
            response_auth_1.json["token"] + "wrong token", 1, "Jack"
        )
        self.assertEqual(response_send.status_code, 401)

        response_send = self.send_item(response_auth_1.json["token"], 1, "Peter")
        self.assertEqual(response_send.status_code, 404)

        response_send = self.send_item(response_auth_1.json["token"], 33, "Jack")
        self.assertEqual(response_send.status_code, 404)

    def test_valid_get_item(self):
        _ = self.register("Tom", "1234")
        response_auth_1 = self.login("Tom", "1234")
        _ = self.create_item(response_auth_1.json["token"], "banana")
        _ = self.create_item(response_auth_1.json["token"], "milk")

        _ = self.register("Jack", "1234")
        response_auth_2 = self.login("Jack", "1234")

        response_send = self.send_item(response_auth_1.json["token"], 1, "Jack")
        query = urlparse.urlparse(response_send.json["link"]).query
        data = parse_qs(query)['data']
        response_get = self.get_item(
            response_auth_2.json["token"], data[0]
        )

        self.assertEqual(response_get.status_code, 200)
        
    def test_invalid_get_item(self):
        _ = self.register("Tom", "1234")
        response_auth_1 = self.login("Tom", "1234")
        _ = self.create_item(response_auth_1.json["token"], "banana")
        _ = self.create_item(response_auth_1.json["token"], "milk")

        _ = self.register("Jack", "1234")
        _ = self.login("Jack", "1234")
        
        
        _ = self.register("Peter", "1234")
        response_auth_3 = self.login("Peter", "1234")

        response_send = self.send_item(response_auth_1.json["token"], 1, "Jack")
        query = urlparse.urlparse(response_send.json["link"]).query
        data = parse_qs(query)['data']
        response_get = self.get_item(
            response_auth_3.json["token"], data[0]
        )

        self.assertEqual(response_get.status_code, 403)
    # ########################
    # #### helper methods ####
    # ########################

    def register(self, login, password):
        return self.app.post(
            "/registration",
            json={"login": login, "password": password},
            follow_redirects=True,
        )

    def login(self, login, password):
        return self.app.post(
            "/login", json={"login": login, "password": password}, follow_redirects=True
        )

    def create_item(self, token, name):
        return self.app.post(
            "/items/new", json={"token": token, "name": name}, follow_redirects=True
        )

    def delete_item(self, token, id):
        return self.app.delete(
            f"/items/{id}", json={"token": token}, follow_redirects=True
        )

    def get_items(self, token):
        return self.app.get(
            "/items", query_string={"token": token}, follow_redirects=True
        )

    def send_item(self, token, id, login):
        return self.app.post(
            "/send",
            json={"token": token, "id": id, "login": login},
            follow_redirects=True,
        )

    def get_item(self, token, data):
        return self.app.get(
            "/get", query_string={"token": token, "data": data}, follow_redirects=True
        )


# if __name__ == "__main__":
#     unittest.main()
