from datetime import datetime
from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from flask_jwt_extended import jwt_required
from .. import db
from ..models import Item

# Define Namespace
item_ns = Namespace("Item", description="Item operations for items")

# Define Request Models for Swagger
item_model = item_ns.model(
    'Item',
    {
        'name': fields.String(required=True, description='The name of the item'),
        'description': fields.String(required=True, description='The description of the item'),
    }
)

item_update_model = item_ns.model(
    'ItemUpdate',
    {
        'name': fields.String(description='The updated name of the item'),
        'description': fields.String(description='The updated description of the item'),
    }
)

# Define API Routes with Swagger Documentation
@item_ns.route('/')
class ItemList(Resource):
    @item_ns.expect(item_model, validate=True)
    @item_ns.response(201, 'Item created successfully')
    @item_ns.response(400, 'Invalid input')
    @jwt_required()
    def post(self):
        """
        Create a new item
        """
        data = request.get_json()
        print("Data :: ",data)
        item = Item(name=data['name'], description=data['description'], created_at=datetime.utcnow())
        db.session.add(item)
        db.session.commit()
        return {'message': 'Item created successfully'}, 201

    @item_ns.response(200, 'Success')
    @jwt_required()
    def get(self):
        """
        Get all items
        """
        items = Item.query.all()
        print("items :: ",items)
        return [{'id': item.id, 'name': item.name, 'description': item.description} for item in items], 200


@item_ns.route('/<int:id>')
@item_ns.param('id', 'The item identifier')
class ItemDetail(Resource):
    @item_ns.expect(item_update_model, validate=True)
    @item_ns.response(200, 'Item updated successfully')
    @item_ns.response(404, 'Item not found')
    @jwt_required()
    def put(self, id):
        """
        Update an item
        """
        data = request.get_json()
        item = Item.query.get_or_404(id)
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        db.session.commit()
        return {'message': 'Item updated successfully'}, 200

    @item_ns.response(200, 'Item deleted successfully')
    @item_ns.response(404, 'Item not found')
    @jwt_required()
    def delete(self, id):
        """
        Delete an item
        """
        item = Item.query.get_or_404(id)
        db.session.delete(item)
        db.session.commit()
        return {'message': 'Item deleted successfully'}, 200
