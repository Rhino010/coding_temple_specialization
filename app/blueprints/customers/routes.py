from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import customer_schema, customers_schema
from flask import Flask, request, jsonify
from marshmallow import ValidationError
from app.models import Customer, db
from sqlalchemy import select, delete


# -----------------------Customer Routes-------------------------------

@customers_bp.route("/", methods=['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
        print(customer_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201
@customers_bp.route("/", methods=["GET"])
def get_customers():
    query = select(Customer)
    result = db.session.execute(query).scalars().all()

    return customers_schema.jsonify(result), 200

@customers_bp.route("/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    if customer == None:
        return jsonify({"Message": "invalid customer id"})
        
    try:
        customer_data = customer_schema.load(request.json)
        print(customer_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
        
    for field, value in customer_data.items():
        setattr(customer, field, value)
    
    db.session.commit()
    return customer_schema.jsonify(customer), 200
    
@customers_bp.route("/<int:customer_id>", methods = ['DELETE'])
def delete_customer(customer_id):

    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message" : f"{customer_id} customer deleted successfully"})
