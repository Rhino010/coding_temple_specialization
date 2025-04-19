from flask import Blueprint

service_tickets_bp = Blueprint('service_tickets_bp', __name__)
service_ticket_items_bp = Blueprint('service_ticket_items_bp', __name__)

from . import routes