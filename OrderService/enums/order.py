from enum import Enum

class Order(Enum):
    PRODUCT_ID = 'productId'
    MERCHANT_ID = 'merchantId'
    BUYER_ID = 'buyerId'
    CREDIT_CARD = 'creditCard'
    DISCOUNT = 'discount'
