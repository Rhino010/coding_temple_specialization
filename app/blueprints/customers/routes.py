from app.blueprints.customers import customers_bp
from app.blueprints.customers.schemas import customer_schema, customers_schema, login_schema
from flask import Flask, request, jsonify
from marshmallow import ValidationError
from app.models import Customer, ServiceTicket, db
from sqlalchemy import select, delete
from app.extensions import limiter, cache
from app.utils.util import encode_token, token_required
from app.blueprints.service_tickets.schemas import service_ticket_schema, service_tickets_schema



# -----------------------Customer Routes-------------------------------
@customers_bp.route("/login", methods=["POST"])
def login():
    try:
        credentials = login_schema.load(request.json)
        email = credentials['email']
        password = credentials['password']

    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == email)
    customer = db.session.execute(query).scalars().first()

    if customer and customer.password == password:
        token = encode_token(customer.id)

        response = {
            "status": "success",
            "message": "login successful",
            "token": token
        }

        return jsonify(response), 200
    
    else:
        return jsonify({"message": "Invalid email or password."})


@customers_bp.route("/", methods=['POST'])
@limiter.limit("3 per hour")
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
        print(customer_data)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'], password=customer_data['password'])
    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer), 201
@customers_bp.route("/", methods=["GET"])
@cache.cached(timeout=60)
def get_customers():

    try:
        page = int(request.args.get('page'))
        per_page = int(request.args.get('per_page'))
        query = select(Customer)
        customers = db.paginate(query, page=page, per_page=per_page)
        return customers_schema.jsonify(customers), 200
    except:
        query = select(Customer)
        result = db.session.execute(query).scalars().all()

    return customers_schema.jsonify(result), 200

@customers_bp.route("/", methods=["PUT"])
@token_required
@limiter.limit("3 per hour")
# There should not be a reason to update customer details very often
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
    
@customers_bp.route("/", methods = ['DELETE'])
@token_required
def delete_customer(customer_id):

    query = select(Customer).where(Customer.id == customer_id)
    customer = db.session.execute(query).scalars().first()

    db.session.delete(customer)
    db.session.commit()

    return jsonify({"message" : f"{customer_id} customer deleted successfully"})

# @customers_bp.route("/service_tickets", methods=["GET"])
# @token_required
# def get_customer_tickets(customer_id):
#     try:
#         query = select(ServiceTicket).where(ServiceTicket.customer_id == customer_id)
#         customer_tickets = db.session.execute(query)
#         ticket_rows = customer_tickets.mappings().all()

#     except ValidationError as e:
#         return jsonify(e.messages), 400

#     db.session.commit()

#     return jsonify(ticket_rows)
