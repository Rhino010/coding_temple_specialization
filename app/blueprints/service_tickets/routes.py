from app.blueprints.service_tickets import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import Flask, request, jsonify
from marshmallow import ValidationError
from app.models import ServiceTicket, db, Mechanic
from sqlalchemy import select, delete



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
            return jsonify({"message": "invalid book id"})

    db.session.add(new_service_ticket)
    db.session.commit()
    
    return service_ticket_schema.jsonify(new_service_ticket)

@service_tickets_bp.route("/", methods=["GET"])
def get_service_tickets():
    query = select(ServiceTicket)
    result = db.session.execute(query).scalars().all()

    return service_tickets_schema.jsonify(result), 200