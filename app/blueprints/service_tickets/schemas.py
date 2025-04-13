from app.models import ServiceTicket
from app.extensions import ma
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
        mechanics = fields.Nested("MechanicSchema", many=True)
        customer = fields.Nested("CustomerSchema")
        class Meta:
                model = ServiceTicket
                fields = ("customer_id", "mechanic_ids", "date", "serv_desc", "vin", "mechanics", "customer")

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
