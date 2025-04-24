from app import create_app
from app.models import db,ServiceTicket, Customer, Mechanic, Inventory
from app.utils.util import encode_token
from datetime import date, datetime
import unittest

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        # Look into the date object necessities when testing with datetime
        self.service_ticket = ServiceTicket(date=datetime.today(), serv_desc="test service description", vin="test777", customer_id=1)
        self.customer = Customer(name="test_user", email="test@email.com", phone="456-789-1234" , password='test')
        self.mechanic = Mechanic(name="test_name", email="test_email@email.com", phone="111-111-1111", salary=12345.03)
        self.mechanic2 = Mechanic(name="test_mechanic", email="test_mechanic@email.com", phone="111-222-1111", salary=22345.03)
        self.inventory = Inventory(part_name="test_part", price=15.01)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.customer)
            db.session.commit()
            db.session.add_all([self.service_ticket, self.mechanic, self.inventory, self.mechanic2])
            db.session.commit()
            self.service_ticket_id = self.service_ticket.id
        self.client = self.app.test_client()
        self.token = encode_token(1)
        self.service_ticket_id = self.service_ticket.id

    def test_create_service_ticket(self):
        service_ticket_payload = {
            'mechanic_ids': [1],
            'date': '1900-01-01',
            'serv_desc': 'test brakes',
            'vin': 'fffff5555',
            'customer_id': 1
        }

        response = self.client.post('/service_tickets/', json=service_ticket_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['customer_id'], 1)

    def test_get_service_tickets(self):

        headers = {'Authorization': "Bearer " + self.token}
        response = self.client.get('/service_tickets/my_tickets', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['serv_desc'], 'test service description')

    def test_get_service_ticket_by_id(self):
        update_payload = {
            "add_mechanic_ids": [2],
            "remove_mechanic_ids": [1]
        }

        response = self.client.put(f'/service_tickets/{self.service_ticket_id}', json=update_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['mechanics'][0]['id'], 2)

    def test_add_service_inventory(self):
        service_inventory_payload = {
            "service_ticket_id": 1,
            "inventory_id": 1,
            "quantity": 10
        }

        response = self.client.post('/service_ticket_items/', json=service_inventory_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["quantity"],10)


        # def test_update_mechanic(self):
    #     update_payload = {
    #         'name': 'john',
    #         'email': 'test_email@email.com',
    #         'phone': '777-777-7777',
    #         'salary': 12345.03
    #     }

    #     response = self.client.put(f'/mechanics/{self.mechanic_id}', json=update_payload)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(response.json['name'], 'john')

    # python -m unittest discover tests

    # venv\Scripts\activate