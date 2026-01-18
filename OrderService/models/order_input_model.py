from dataclasses import dataclass
from OrderService.clients.buyer_client import BuyerClient
from OrderService.clients.inventory_client import InventoryClient
from OrderService.clients.merchant_client import MerchantClient


@dataclass
class CreditCardInputModel:
    card_number: int
    expiration_month: int
    expiration_year: int
    cvc: int

class OrderInputModel:

    def __init__(self, product_id: str, merchant_id: str, buyer_id: str, credit_card: CreditCardInputModel, discount: float):
        self.product_id = product_id
        self.merchant_id = merchant_id
        self.buyer_id = buyer_id
        self.credit_card = credit_card
        self.discount = discount
        self.__error_string = ''
        self.__status_code = None


    def __get_buyer_response(self, buyer_client):
        return buyer_client.get_buyer_by_id(self.buyer_id)

    def __get_merchant_response(self, merchant_client):
        return merchant_client.get_merchant_by_id(self.merchant_id)

    def __get_product_response(self, inventory_client):
        return inventory_client.get_product_by_id(self.product_id)

    def retrieve_error_string(self):
        return self.__error_string

    def retrieve_status_code(self):
        return self.__status_code


    def is_valid(self):
        merchant_response = self.__get_merchant_response(MerchantClient())
        buyer_response = self.__get_buyer_response(BuyerClient())
        product_response = self.__get_product_response(InventoryClient())

        if not self.__does_merchant_exist(merchant_response):
            self.__error_string = 'Merchant does not exist'
            self.__status_code = 400
            return False
        if not self.__does_buyer_exist(buyer_response):
            self.__error_string = 'Buyer does not exist'
            self.__status_code = 400
            return False
        if not self.__does_product_exist(product_response):
            self.__error_string = 'Product does not exist'
            self.__status_code = 400
            return False

        if not self.__is_merchant_ok(merchant_response):
            self.__error_string = 'Merchant not ok'
            self.__status_code = merchant_response['status_code']
            return False
        if not self.__is_buyer_ok(buyer_response):
            self.__error_string = 'Buyer not ok'
            self.__status_code = buyer_response['status_code']
            return False
        if not self.__is_product_ok(product_response):
            self.__error_string = 'Product not ok'
            self.__status_code = product_response['status_code']
            return False
        merchant = merchant_response['data']
        buyer = buyer_response['data']
        product = product_response['data']

        if not self.__is_product_in_stock(product):
            self.__error_string = 'Product is sold out'
            self.__status_code = 400
            return False
        if not self.__does_product_belong_to_merchant(product):
            self.__error_string = 'Product does not belong to merchant'
            self.__status_code = 400
            return False
        if not self.__does_merchant_allow_discount(merchant):
            self.__error_string = 'Merchant does not allow discount'
            self.__status_code = 400
            return False

        return True


    # OrderService; shouldreturn 400; HTTP; Status; Codewith the error message "Merchant does not exist;" if there is
    # no merchant with the specific id
    def __does_merchant_exist(self, merchant_response):
        return False if merchant_response['status_code'] == 404 else True

    # OrderService; shouldreturn 400; HTTP; Status; Codewith the error message "Buyer does not exist;" if there is not
    # buyer with the specific buyerId
    def __does_buyer_exist(self, buyer_response):
        return False if buyer_response['status_code'] == 404 else True

    # OrderService; shouldreturn 400; HTTP; Status; Codewith the error message "Product does not exist;" if there is
    # no product with the specific productId
    def __does_product_exist(self, product_response):
        return False if product_response['status_code'] == 404 else True

    # OrderService; shouldreturn 400; HTTP; Status; Codewith the error message "Product is sold out;" if a product
    # with the specific productId is sold out.
    def __is_product_in_stock(self, product):
        return product['quantity'] - product['reserved'] > 0

    # OrderService; shouldreturn 400; HTTP; Status; Codewith the error message "Product does not belong; to; merchant;"
    # if product with productId does not belong to merchant with merchantId.
    def __does_product_belong_to_merchant(self, product):
        return product['merchantId'] == self.merchant_id

    # OrderService; shouldreturn 400; HTTP; Status; Codewith the error message "Merchant does not allow; discount;" if
    # merchant with merchantId does not allow discounts and the specified; discount is something; other; then; null or 0.
    def __does_merchant_allow_discount(self, merchant):
        return merchant['allowsDiscount']


    def __is_merchant_ok(self, merchant_response):
        return False if merchant_response['status_code'] != 200 else True

    def __is_buyer_ok(self, buyer_response):
        return False if buyer_response['status_code'] != 200 else True

    def __is_product_ok(self, product_response):
        return False if product_response['status_code'] != 200 else True

