from flask import request, Blueprint, jsonify
from WrapperAPI.clients.inventory_client import InventoryClient


product_blueprint = Blueprint('product_endpoints', __name__)

inventory_client = InventoryClient()


@product_blueprint.route('/products/<string:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    response = inventory_client.get_product_by_id(product_id)

    if response['status_code'] != 200:
        message = response['data']['msg']
        status = response['status_code']
        return jsonify({'msg': message, 'status': status}), status

    return jsonify(response['data']), 200

@product_blueprint.route('/products', methods=['POST'])
def create_product():
    req_body = request.get_json()
    response = inventory_client.create_new_product(req_body)

    if response['status_code'] != 201:
        message = response['data']['msg']
        status = response['status_code']
        return jsonify({'msg': message, 'status': status}), status

    return jsonify({'new_id': response['data']['new_id'], 'status': 201}), 201



