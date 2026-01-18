from OrderService.clients.buyer_client import BuyerClient
from OrderService.clients.inventory_client import InventoryClient
from OrderService.clients.merchant_client import MerchantClient
from OrderService.enums.credit_card import CreditCard
from OrderService.enums.order import Order
from OrderService.messaging.exchange import Exchange
from OrderService.models.order_input_model import OrderInputModel
from OrderService.repositories.order_repository import OrderRepository


class OrderService:

    def __init__(self, order_repository: OrderRepository, inventory_client: InventoryClient, buyer_client: BuyerClient,
                 merchant_client: MerchantClient, exchange: Exchange):
        self.__order_repository = order_repository
        self.__inventory_client = inventory_client
        self.__merchant_client = merchant_client
        self.__buyer_client = buyer_client
        self.__exchange = exchange

    def get_order_by_id(self, order_id: int):
        order = self.__order_repository.get_order_by_id(order_id)

        if not order: return None

        card_number = order[CreditCard.CARD_NUMBER.value]
        hidden_card_number = '*'*(len(card_number)-4)
        hidden_card_number+=card_number[len(card_number)-4:]
        order[CreditCard.CARD_NUMBER.value] = hidden_card_number

        return order


    def create_order(self, order: OrderInputModel):
        new_order = self.__order_repository.create_order(order)
        if not new_order: return None

        res = self.__buyer_client.get_buyer_by_id(new_order[Order.BUYER_ID.value])
        if res['status_code'] != 200: return None
        buyer = res['data']

        res = self.__merchant_client.get_merchant_by_id(new_order[Order.MERCHANT_ID.value])
        if res['status_code'] != 200: return None
        merchant = res['data']

        res = self.__inventory_client.get_product_by_id(new_order[Order.PRODUCT_ID.value])
        if res['status_code'] != 200: return None
        product = res['data']

        order_to_send = {
            'id': new_order['id'],
            'buyer_email': buyer['email'],
            'merchant_email': merchant['email'],
            'productId': new_order[Order.PRODUCT_ID.value],
            'product_name': product['productName'],
            Order.CREDIT_CARD.value: new_order[Order.CREDIT_CARD.value],
            'total_price': product['price'] * (1 - float(new_order[Order.DISCOUNT.value]))
        }

        self.__inventory_client.reserve_product_by_id(new_order[Order.PRODUCT_ID.value])
        self.__exchange.send_order_created_event(order_to_send)

        return new_order['id']



