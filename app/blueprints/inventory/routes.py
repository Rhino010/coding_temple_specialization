from app.blueprints.inventory import parts_bp
from app.blueprints.inventory.schemas import part_schema, parts_schema
from flask import Flask, request, jsonify
from marshmallow import ValidationError
from app.models import Inventory, db
from sqlalchemy import select




@parts_bp.route("/", methods=['POST'])
def create_part():
    try:
        part_data = part_schema.load(request.json)
        print(part_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_part = Inventory(part_name=part_data['part_name'], price=part_data['price'])
    db.session.add(new_part)
    db.session.commit()

    return part_schema.jsonify(new_part), 200

@parts_bp.route("/", methods=["GET"])
def get_parts():
    query = select(Inventory)
    result = db.session.execute(query).scalars().all()

    return parts_schema.jsonify(result), 200

@parts_bp.route("/<int:part_id>", methods=["PUT"])
def update_part(part_id):
    query = select(Inventory).where(Inventory.id == part_id)
    part = db.session.execute(query).scalars().first()

    if part == None:
        return jsonify({"Message": "invalid part id"})
    
    try:
        part_data = part_schema.load(request.json)
        print(part_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for field, value in part_data.items():
        setattr(part, field, value)

    db.session.commit()
    return part_schema.jsonify(part), 200
    
@parts_bp.route("/<int:part_id>", methods = ['DELETE'])
def delete_part(part_id):

    query = select(Inventory).where(Inventory.id == part_id)
    part = db.session.execute(query).scalars().first()

    db.session.delete(part)
    db.session.commit()

    return jsonify({"message" : f"Part {part_id} deleted successfully"})

