from app import create_app
from app.models import db,ServiceTicket
# from app.utils.util import encode_token
from datetime import date, datetime
import unittest

class TestMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.service_ticket = ServiceTicket(date=datetime.today(), serv_desc="test service description", vin="test777", customer_id=1)
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.service_ticket)
            db.session.commit()
            self.service_ticket_id = self.service_ticket.id
        # self.token = encode_token(1, 'admin')
        self.client = self.app.test_client()

    # def test_create_service_ticket(self):
    #     service_ticket_payload = {
    #         'mechanic_ids': [1],
    #         'date': date.today(),
    #         'serv_desc': 'test brakes',
    #         'vin': 'fffff5555',
    #         'customer_id': 2
    #     }

    #     response = self.client.post('/service_tickets/', json=service_ticket_payload)
    #     self.assertEqual(response.status_code, 400)
    #     self.assertEqual(response.json['customer_id'], 2)

    def test_get_service_tickets(self):

        response = self.client.get('/service_tickets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]['serv_desc'],"test service description")

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