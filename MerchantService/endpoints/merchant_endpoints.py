from flask import request, Blueprint, jsonify
from MerchantService.models.db_config import DbConfig
from MerchantService.enums.merchant import Merchant
from MerchantService.models.merchant_input_model import MerchantInputModel
from MerchantService.repositories.merchant_repository import MerchantRepository

merchant_blueprint = Blueprint('merchant_endpoints', __name__)


merchant_repository = MerchantRepository(DbConfig(
    user='postgres',
    password='postgres',
    database='Merchants',
    host='merchant-service-db'
))


@merchant_blueprint.route('/merchants/<string:merchant_id>', methods=['GET'])
def get_merchant_by_id(merchant_id):
    merchant = merchant_repository.get_merchant_by_id(merchant_id)

    if not merchant:
        return jsonify({'msg': f'Merchant with id {merchant_id} not found', 'status': 404}), 404

    return jsonify(merchant), 200

@merchant_blueprint.route('/merchants', methods=['POST'])
def create_merchant():
    req_body = request.get_json()

    try:
        merchant = MerchantInputModel(
            name = req_body[Merchant.NAME.value],
            ssn = req_body[Merchant.SSN.value],
            email = req_body[Merchant.EMAIL.value],
            phone_number = req_body[Merchant.PHONE_NUMBER.value],
            allows_discount = req_body[Merchant.ALLOWS_DISCOUNT.value]
        )
    except KeyError as e:
        return jsonify({"msg": f"Request body missing required attribute {str(e)}", "status": 412}), 412

    new_id = merchant_repository.create_merchant(merchant)

    if not new_id:
        return jsonify({'msg': 'Failed to create merchant', 'status': 500}), 500

    return jsonify({'new_id': new_id, 'status': 201}), 201




