from app import create_app
from app.models import db,Customer
# from app.utils.util import encode_token
import unittest

class TestCustomer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.customer = Customer(name="test_user", email="test@email.com", phone="456-789-1234" , password='test')
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
        # self.token = encode_token(1, 'admin')
        self.client = self.app.test_client()

    def test_create_customer(self):
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "111-111-1111",
            "password": "123"
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'John Doe')

    def test_invalid_creation(self):
        customer_payload = {
            "name": "John Doe",
            "email": "jd@email.com",
            "phone": "111-111-1111",
        }

        response = self.client.post('/customers/', json=customer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['password'], ['Missing data for required field.'])

    def test_login_customer(self):
        credentials = {
            "email": "test@email.com",
            "password": "test"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], 'success')
        print(response.json['token'])
        return response.json['token']

    def test_invalid_login(self):
        credentials = {
            "email": "bad_email@email.com",
            "password": "bad_pw"
        }

        response = self.client.post('/customers/login', json=credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], 'Invalid email or password.')

    def test_get_all_customers(self):

        response = self.client.get('/customers/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['name'], 'test_user')

    def test_update_customer(self):
        update_payload = {
            "name": "updated_user",
            "email": "test@email.com",
            "phone": "456-789-1234",
            "password": "test"
        }

        headers = {'Authorization': "Bearer " + self.test_login_customer()}
        response = self.client.put('/customers/', json=update_payload, headers=headers)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.json['name'], 'updated_user')
        self.assertEqual(response.json['email'], 'test@email.com')

        # def (self):

    #     response = self.client.post('/customers/', json=)
    #     self.assertEqual(response.status_code,)
    #     self.assertEqual(response.json)

        # def (self):

    #     response = self.client.post('/customers/', json=)
    #     self.assertEqual(response.status_code,)
    #     self.assertEqual(response.json)


# python -m unittest discover tests