from flask import request, Blueprint, jsonify
from Gateway.clients.order_client import OrderClient


order_blueprint = Blueprint('order_endpoints', __name__)

order_client = OrderClient()


@order_blueprint.route('/orders/<string:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    response = order_client.get_order_by_id(order_id)

    if response['status_code'] != 200:
        message = response['data']['msg']
        status = response['status_code']
        return jsonify({'msg': message, 'status': status}), status

    return jsonify(response['data']), 200


@order_blueprint.route('/orders', methods=['POST'])
def create_order():
    req_body = request.get_json()
    response = order_client.create_new_order(req_body)

    if response['status_code'] != 201:
        message = response['data']['msg']
        status = response['status_code']
        return jsonify({'msg': message, 'status': status}), status

    return jsonify({'new_id': response['data']['new_id'], 'status': 201}), 201




