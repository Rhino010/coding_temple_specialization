from app.blueprints.service_tickets import service_tickets_bp, service_ticket_items_bp
from .schemas import service_ticket_schema, service_tickets_schema, edit_service_schema,return_ticket_schema, create_service_inventory_schema
from flask import Flask, request, jsonify
from marshmallow import ValidationError
from app.models import ServiceTicket, db, Mechanic, ServiceTicketItems
from sqlalchemy import select, delete
from app.extensions import cache
from app.utils.util import token_required




@service_tickets_bp.route("/", methods=["POST"])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
        print(service_ticket_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_service_ticket = ServiceTicket(date=service_ticket_data["date"], serv_desc=service_ticket_data["serv_desc"], vin=service_ticket_data["vin"], customer_id=service_ticket_data["customer_id"])

    for mechanic_id in service_ticket_data["mechanic_ids"]:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalar()
        if mechanic:
            new_service_ticket.mechanics.append(mechanic)
        else:
            return jsonify({"message": "invalid mechanic id"})

    db.session.add(new_service_ticket)
    db.session.commit()
    
    return service_ticket_schema.jsonify(new_service_ticket)

@service_tickets_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
def get_service_tickets():
    query = select(ServiceTicket)
    result = db.session.execute(query).scalars().all()

    return service_tickets_schema.jsonify(result), 200

@service_tickets_bp.route("/my_tickets", methods=["GET"])
@token_required
def get_customer_tickets(customer_id):
    query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
    customer_record = db.session.execute(query).scalars()

    return service_tickets_schema.jsonify(customer_record), 200

@service_tickets_bp.route("/<int:service_ticket_id>", methods=["PUT"])
def edit_service_ticket(service_ticket_id):
    
    try:
        service_ticket_edits = edit_service_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    

    query = select(ServiceTicket).where(ServiceTicket.id == service_ticket_id)
    service_ticket = db.session.execute(query).scalars().first()

    for mechanic_id in service_ticket_edits['add_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic not in service_ticket.mechanics:
            service_ticket.mechanics.append(mechanic)

    for mechanic_id in service_ticket_edits['remove_mechanic_ids']:
        query = select(Mechanic).where(Mechanic.id == mechanic_id)
        mechanic = db.session.execute(query).scalars().first()

        if mechanic and mechanic in service_ticket.mechanics:
            service_ticket.mechanics.remove(mechanic)
    
    db.session.commit()
    return return_ticket_schema.jsonify(service_ticket), 200 


@service_ticket_items_bp.route('/', methods=['POST'])
def add_service_inventory():
    try:
        service_ticket_data =  create_service_inventory_schema.load(request.json)
    
    except ValidationError as e:
        return jsonify(e.messages), 400

    new_ticket_inventory = ServiceTicketItems(service_ticket_id=service_ticket_data['service_ticket_id'], inventory_id=service_ticket_data["inventory_id"], quantity=service_ticket_data['quantity'])

    db.session.add(new_ticket_inventory)
    db.session.commit()

    return create_service_inventory_schema.jsonify(new_ticket_inventory), 200




    # service_ticket_id: Mapped[int] = mapped_column(db.ForeignKey("service_tickets.id"),nullable=False)
    # inventory_id: Mapped[int] = mapped_column(db.ForeignKey("inventory.id"), nullable=False)
    # quantity: Mapped[int] = mapped_column(nullable=False)