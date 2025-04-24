from app import create_app
from app.models import db,Mechanic
# from app.utils.util import encode_token
import unittest

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.mechanic = Mechanic(name="test_name", email="test_email@email.com", phone="111-111-1111", salary=12345.03)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
            self.mechanic_id = self.mechanic.id
        # self.token = encode_token(1, 'admin')
        self.client = self.app.test_client()


    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "jason jason",
            "email": "email@email.com",
            "phone": "777-777-7777",
            "salary": 11111.11
        }

        response = self.client.post('/mechanics/', json=mechanic_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], 'jason jason')

    
    def test_get_mechanics(self):

        response = self.client.get('/mechanics/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['email'], 'test_email@email.com')

    
    def test_update_mechanic(self):
        update_payload = {
            'name': 'john',
            'email': 'test_email@email.com',
            'phone': '777-777-7777',
            'salary': 12345.03
        }

        response = self.client.put(f'/mechanics/{self.mechanic_id}', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'john')

    
    def test_delete_mechanic(self):

        response = self.client.delete(f'/mechanics/{self.mechanic_id}')
        self.assertEqual(response.status_code, 200)


    # python -m unittest discover tests