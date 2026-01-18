from flask import request, Blueprint, jsonify
from BuyerService.models.db_config import DbConfig
from BuyerService.enums.buyer import Buyer
from BuyerService.models.buyer_input_model import BuyerInputModel
from BuyerService.repositories.buyer_repository import BuyerRepository

buyer_blueprint = Blueprint('buyer_endpoints', __name__)


buyer_repository = BuyerRepository(DbConfig(
    user='postgres',
    password='postgres',
    database='Buyers',
    host='buyer-service-db'
))


@buyer_blueprint.route('/buyers/<string:buyer_id>', methods=['GET'])
def get_buyer_by_id(buyer_id):
    buyer = buyer_repository.get_buyer_by_id(buyer_id)

    if not buyer:
        return jsonify({'msg': f'Buyer with id {buyer_id} not found', 'status': 404}), 404

    return jsonify(buyer), 200

@buyer_blueprint.route('/buyers', methods=['POST'])
def create_buyer():
    req_body = request.get_json()

    try:
        buyer = BuyerInputModel(
            name = req_body[Buyer.NAME.value],
            ssn = req_body[Buyer.SSN.value],
            email = req_body[Buyer.EMAIL.value],
            phone_number = req_body[Buyer.PHONE_NUMBER.value],
        )
    except KeyError as e:
        return jsonify({"msg": f"Request body missing required attribute {str(e)}", "status": 412}), 412

    new_id = buyer_repository.create_buyer(buyer)

    if not new_id:
        return jsonify({'msg': 'Failed to create buyer', 'status': 500}), 500

    return jsonify({'new_id': new_id, 'status': 200}), 201




