from app.models import Inventory
from app.extensions import ma


class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory

part_schema = InventorySchema()
parts_schema = InventorySchema(many=True)