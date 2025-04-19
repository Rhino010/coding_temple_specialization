from app.blueprints.mechanics import mechanics_bp
from app.blueprints.mechanics.schemas import mechanic_schema, mechanics_schema
from flask import Flask, request, jsonify
from marshmallow import ValidationError
from app.models import Mechanic, db
from sqlalchemy import select, delete
from app.extensions import limiter, cache

# ------------------------------Mechanic Routes----------------------------------------------
@mechanics_bp.route("/", methods=['POST'])
@limiter.limit("3 per hour")
# adding limits to post routes to prevent spamming new mechanics
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
        print(mechanic_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_mechanic = Mechanic(name=mechanic_data['name'], email=mechanic_data['email'], phone=mechanic_data['phone'], salary=mechanic_data['salary'])
    db.session.add(new_mechanic)
    db.session.commit()

    return mechanic_schema.jsonify(new_mechanic), 201

@mechanics_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
def get_mechanics():
    query = select(Mechanic)
    result = db.session.execute(query).scalars().all()

    return mechanics_schema.jsonify(result), 200

@mechanics_bp.route("/<int:mechanic_id>", methods=["PUT"])
@limiter.limit("3 per hour")
# should not be a reason to update details of employees that often
def update_mechanic(mechanic_id):
    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

    if mechanic == None:
        return jsonify({"Message": "invalid mechanic id"})
        
    try:
        mechanic_data = mechanic_schema.load(request.json)
        print(mechanic_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
        
    for field, value in mechanic_data.items():
        setattr(mechanic, field, value)
    
    db.session.commit()
    return mechanic_schema.jsonify(mechanic), 200
    
@mechanics_bp.route("/<int:mechanic_id>", methods = ['DELETE'])
def delete_mechanic(mechanic_id):

    query = select(Mechanic).where(Mechanic.id == mechanic_id)
    mechanic = db.session.execute(query).scalars().first()

    db.session.delete(mechanic)
    db.session.commit()

    return jsonify({"message" : f"{mechanic_id} mechanic deleted successfully"})

@mechanics_bp.route("/popular", methods=["GET"])
def popular_books():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()

    mechanics.sort(key = lambda mechanic: len(mechanic.service_tickets), reverse=True)

    return mechanics_schema.jsonify(mechanics)
