from app.models import ServiceTicket, ServiceTicketItems
from app.extensions import ma
from marshmallow import fields

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
        mechanics = fields.Nested("MechanicSchema", many=True)
        customer = fields.Nested("CustomerSchema")

        class Meta:
                model = ServiceTicket
                fields = ("id", "customer_id", "mechanic_ids", "date", "serv_desc", "vin", "mechanics", "customer")

class EditServiceSchema(ma.Schema):
    add_mechanic_ids = fields.List(fields.Int(), required=True)
    remove_mechanic_ids = fields.List(fields.Int(), required=True)

    class Meta:
           fields=("add_mechanic_ids", "remove_mechanic_ids")

class ServiceTicketPartSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicketItems
    part = fields.Nested("InventorySchema", exclude=["id"])

class CreateServiceInventorySchema(ma.Schema):
      service_ticket_id = fields.Int(required=True)
      inventory_id = fields.Int(required=True)
      quantity = fields.Int(required=True)


service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
return_ticket_schema = ServiceTicketSchema(exclude=["customer_id"])
edit_service_schema = EditServiceSchema()
create_service_inventory_schema = CreateServiceInventorySchema()
