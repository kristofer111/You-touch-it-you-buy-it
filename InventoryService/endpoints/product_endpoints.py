from flask import request, Blueprint, jsonify
from InventoryService.models.db_config import DbConfig
from InventoryService.enums.product import Product
from InventoryService.models.product_input_model import ProductInputModel
from InventoryService.repositories.product_repository import ProductRepository

product_blueprint = Blueprint('product_endpoints', __name__)

product_repository = ProductRepository(DbConfig(
    user='postgres',
    password='postgres',
    database='Inventory',
    host='inventory-service-db'
))


@product_blueprint.route('/products/<string:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = product_repository.get_product_by_id(product_id)

    if not product:
        return jsonify({'msg': f'Product does not exits', 'status': 404}), 404

    return jsonify(product), 200

@product_blueprint.route('/products', methods=['POST'])
def create_product():
    req_body = request.get_json()

    try:
        product = ProductInputModel(
            merchant_id = req_body[Product.MERCHANT_ID.value],
            product_name = req_body[Product.PRODUCT_NAME.value],
            price = req_body[Product.PRICE.value],
            quantity = req_body[Product.QUANTITY.value],
        )
    except KeyError as e:
        return jsonify({"msg": f"Request body missing required attribute {str(e)}", "status": 412}), 412

    new_id = product_repository.create_product(product)

    if not new_id:
        return jsonify({'msg': 'Failed to create product', 'status': 500}), 500

    return jsonify({'new_id': new_id, 'status': 201}), 201

@product_blueprint.route('/products/<string:product_id>/reserve', methods=['PATCH'])
def reserve_product_by_id(product_id):
    product_repository.reserve_product_by_id(product_id)

    return {'msg': 'Product reserved successfully', 'status': 200}, 200



