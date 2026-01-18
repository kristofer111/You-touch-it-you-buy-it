from flask import request, Blueprint, jsonify
from Gateway.clients.merchant_client import MerchantClient

merchant_blueprint = Blueprint('merchant_endpoints', __name__)

merchant_client = MerchantClient()


@merchant_blueprint.route('/merchants/<string:merchant_id>', methods=['GET'])
def get_merchant_by_id(merchant_id):
    response = merchant_client.get_merchant_by_id(merchant_id)

    if response['status_code'] != 200:
        message = response['data']['msg']
        status = response['status_code']
        return jsonify({'msg': message, 'status': status}), status

    return jsonify(response['data']), 200

@merchant_blueprint.route('/merchants', methods=['POST'])
def create_merchant():
    req_body = request.get_json()
    response = merchant_client.create_new_merchant(req_body)

    if response['status_code'] != 201:
        message = response['data']['msg']
        status = response['status_code']
        return jsonify({'msg': message, 'status': status}), status

    return jsonify({'new_id': response['data']['new_id'], 'status': 201}), 201