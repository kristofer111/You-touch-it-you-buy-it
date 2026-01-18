from flask import request, Blueprint, jsonify
from WrapperAPI.clients.buyer_client import BuyerClient

buyer_blueprint = Blueprint('buyer_endpoints', __name__)
buyer_client = BuyerClient()


@buyer_blueprint.route('/buyers/<string:buyer_id>', methods=['GET'])
def get_buyer_by_id(buyer_id):
    response = buyer_client.get_buyer_by_id(buyer_id)

    if response['status_code'] != 200:
        message = response['data']['msg']
        status = response['status_code']
        return jsonify({'msg': message, 'status': status}), status

    return jsonify(response['data']), 200

@buyer_blueprint.route('/buyers', methods=['POST'])
def create_buyer():
    req_body = request.get_json()
    response = buyer_client.create_new_buyer(req_body)

    if response['status_code'] != 201:
        message = response['data']['msg']
        status = response['status_code']
        return jsonify({'msg': message, 'status': status}), status

    return jsonify({'new_id': response['data']['new_id'], 'status': 201}), 201




