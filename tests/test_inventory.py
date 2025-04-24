from app import create_app
from app.models import db,Inventory
# from app.utils.util import encode_token
import unittest

class TestInventory(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.inventory = Inventory(part_name="test_part", price=15.01)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.inventory)
            db.session.commit()
            self.inventory_id = self.inventory.id
        # self.token = encode_token(1, 'admin')
        self.client = self.app.test_client()

# Post, get, put w/id, delete w/id

    def test_create_inventory(self):
        inventory_payload = {
            "part_name" : "tire",
            "price": 1.99
        }

        response = self.client.post('/inventory/', json=inventory_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['part_name'], "tire")

    def test_get_inventory(self):

        response = self.client.get('/inventory/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['part_name'], 'test_part')

    def test_update_inventory(self):
        update_payload = {
            "part_name": "updated_part",
            "price": 1.29
        }

        response = self.client.put(f'/inventory/{self.inventory_id}', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['part_name'], 'updated_part')

    def delete_inventory(self):
        
        response = self.client.delete(f'/inventory/{self.inventory_id}')
        self.assertEqual(response.status_code, 200)


# python -m unittest discover tests