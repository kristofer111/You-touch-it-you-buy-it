from flask import request, Blueprint, jsonify
from OrderService.clients.buyer_client import BuyerClient
from OrderService.clients.inventory_client import InventoryClient
from OrderService.clients.merchant_client import MerchantClient
from OrderService.messaging.exchange import Exchange
from OrderService.models.db_config import DbConfig
from OrderService.enums.credit_card import CreditCard
from OrderService.enums.order import Order
from OrderService.models.order_input_model import OrderInputModel, CreditCardInputModel
from OrderService.repositories.order_repository import OrderRepository
from OrderService.services.order_service import OrderService


order_blueprint = Blueprint('order_endpoints', __name__)

db_config = DbConfig(
    user='postgres',
    password='postgres',
    database='Orders',
    host='order-service-db'
)
order_repository = OrderRepository(db_config, InventoryClient())
order_service = OrderService(order_repository, InventoryClient(), BuyerClient(), MerchantClient(), Exchange())


@order_blueprint.route('/orders/<string:order_id>', methods=['GET'])
def get_order_by_id(order_id):
    order = order_service.get_order_by_id(order_id)

    if not order:
        return jsonify({'msg': 'Order does not exist', 'status': 404}), 404

    return jsonify(order), 200

@order_blueprint.route('/orders', methods=['POST'])
def create_order():
    req_body = request.get_json()

    try:
        req_body_card = req_body[Order.CREDIT_CARD.value]
        credit_card = CreditCardInputModel(
            card_number = req_body_card[CreditCard.CARD_NUMBER.value],
            expiration_month = req_body_card[CreditCard.EXPIRATION_MONTH.value],
            expiration_year = req_body_card[CreditCard.EXPIRATION_YEAR.value],
            cvc = req_body_card[CreditCard.CVC.value]
        )

        order = OrderInputModel(
            product_id = req_body[Order.PRODUCT_ID.value],
            merchant_id = req_body[Order.MERCHANT_ID.value],
            buyer_id = req_body[Order.BUYER_ID.value],
            credit_card = credit_card,
            discount = req_body[Order.DISCOUNT.value]
        )
    except KeyError as e:
        return jsonify({"msg": f"Request body missing required attribute {str(e)}", "status": 412}), 412

    if not order.is_valid():
        status = order.retrieve_status_code()
        return jsonify({'msg': order.retrieve_error_string(), 'status': status}), status

    new_id = order_service.create_order(order)

    if not new_id:
        return jsonify({'msg': 'Failed to create order', 'status': 500}), 500

    return jsonify({'new_id': new_id, 'status': 201}), 201




