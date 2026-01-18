import json
import luhn
from credit_card import CreditCard


def is_payment_valid(card):
    with open("card_received.json", "w") as file:
        json.dump(card, file, indent=4)

    card_number = card[CreditCard.CARD_NUMBER.value]
    month = card[CreditCard.EXPIRATION_MONTH.value]
    year = card[CreditCard.EXPIRATION_YEAR.value]
    cvc = card[CreditCard.CVC.value]

    return (luhn.verify(card_number) and # "1234" works??
            1 <= month <= 12         and
            len(str(year)) == 4      and
            len(str(cvc)) == 3)

(luhn.verify("1234") and # "1234" works??
            1 <= 8 <= 12         and
            len(str(2025)) == 4      and
            len(str(123)) == 3)

# You will use luhn algorithm to validate the card number
# Month expiration value should be a number within the range 1 til 12
# Year expiration should be a four digit number
# CVC value should be a three digit number.






