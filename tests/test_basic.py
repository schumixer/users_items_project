# project/test_basic.py
import os
import unittest
from flask import request
from users_items_project import app, db
 
TEST_DB = 'test.db'

class BasicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        basedir = os.path.dirname(os.path.abspath(__file__))
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)

    ############################
    #### setup and teardown ####
    ############################
    
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
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_valid_user_registration(self):
        response = self.register('Tom', '1234')
        self.assertEqual(response.status_code, 201)

    # def test_invalid_user_registration(self):
    #     response = self.register('Tom', '1234')
    #     self.assertEqual(response.status_code, 201)
    #     response = self.register('Tom', '12345')
    #     self.assertEqual(response.status_code, 200)
        
        
        
    # def test_valid_user_authorization(self):
    #     response_reg = self.register('Tom', '1234')
    #     response_auth = self.login('Tom', '1234')
    #     self.assertEqual(response.status_code, 200)
        
        
    # def test_invalid_user_authorization(self):
    #     response_reg = self.register('Tom', '1234')
    #     response_auth = self.login('Tom', '12345')
    #     self.assertEqual(response.status_code, 401)
        
        
    # def test_valid_item_creation(self):
    #     response_reg = self.register('Tom', '1234')
    #     response_auth = self.login('Tom', '12345')
        
    #     self.assertEqual(response.status_code, 401)
        
    
    # ########################
    # #### helper methods ####
    # ########################
    
    def register(self, login, password):
        return self.app.post(
            '/registration', json={
                'login': login, 'password': password
                },
            follow_redirects=True
        )
 
    # def login(self, email, password):
    #     return self.app.post(
    #     '/login',
    #     data=dict(email=email, password=password),
    #     follow_redirects=True
    #     )
        
        
    # def create_item(self, email, password):
    #     return self.app.post(
    #     '/items/new',
    #     data=dict(email=email, password=password),
    #     follow_redirects=True
    #    )
 


if __name__ == "__main__":
    unittest.main()