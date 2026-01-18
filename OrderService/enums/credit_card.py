from enum import Enum

class CreditCard(Enum):
    CARD_NUMBER = 'cardNumber'
    EXPIRATION_MONTH = 'expirationMonth'
    EXPIRATION_YEAR = 'expirationYear'
    CVC = 'cvc'