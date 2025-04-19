from flask import Blueprint

parts_bp = Blueprint('parts_bp', __name__)
# Blueprints need to be registered

from . import routes

