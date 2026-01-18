import psycopg2
import psycopg2.extras
from OrderService.models.order_input_model import OrderInputModel
from OrderService.enums.credit_card import CreditCard
from OrderService.enums.order import Order


class OrderRepository:

    def __init__(self, db_config, inventory_client):
        self.__db_config = db_config
        self.__inventory_client = inventory_client

        self.__write('''
            CREATE TABLE IF NOT EXISTS "CreditCards"(
                id INTEGER PRIMARY KEY,
                "cardNumber" VARCHAR(64) NOT NULL,
                "expirationMonth" INTEGER NOT NULL,
                "expirationYear" INTEGER NOT NULL,
                cvc INTEGER NOT NULL
            )
        ''')
        self.__write('''
           CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER PRIMARY KEY, 
                "productId" INTEGER, 
                "merchantId" INTEGER, 
                "buyerId" INTEGER, 
                "creditCardId" INTEGER REFERENCES "CreditCards"(id) ON DELETE SET NULL,
                discount DECIMAL
           )
        ''')


    def __get_connection(self):
        return psycopg2.connect(
            user = self.__db_config.user,
            password = self.__db_config.password,
            database = self.__db_config.database,
            host = self.__db_config.host
        )

    def __read_single(self, execution_string, params=None):
        connection = self.__get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute(execution_string, params) if params else cursor.execute(execution_string)
        row = cursor.fetchone()

        cursor.close()
        connection.close()
        return row

    def __write(self, execution_string, params=None):
        connection = self.__get_connection()
        cursor = connection.cursor()

        cursor.execute(execution_string, params) if params else cursor.execute(execution_string)
        connection.commit()

        cursor.close()
        connection.close()


    def __write_returning(self, execution_string, params=None):
        connection = self.__get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute(execution_string, params) if params else cursor.execute(execution_string)
        row = cursor.fetchone()
        connection.commit()

        cursor.close()
        connection.close()
        return row



    def get_order_by_id(self, order_id):
        execution_string = """
            SELECT o.*, c."cardNumber", c."expirationMonth", c."expirationYear", c.cvc
            FROM Orders AS o 
            LEFT JOIN "CreditCards" AS c ON o."creditCardId" = c.id
            WHERE o.id = %s
        """

        order = self.__read_single(execution_string, (order_id,))
        if not order: return None

        res = self.__inventory_client.get_product_by_id(order[Order.PRODUCT_ID.value])
        if res['status_code'] != 200: return None
        product = res['data']

        return {
            Order.PRODUCT_ID.value: order[Order.PRODUCT_ID.value],
            Order.MERCHANT_ID.value: order[Order.MERCHANT_ID.value],
            Order.BUYER_ID.value: order[Order.BUYER_ID.value],
            CreditCard.CARD_NUMBER.value: order[CreditCard.CARD_NUMBER.value],
            'totalPrice': product['price']*(1-float(order[Order.DISCOUNT.value]))
        }



    def __get_next_order_id(self):
        row = self.__read_single("SELECT COALESCE(MAX(id),0) AS max_id FROM Orders")
        next_id = row['max_id'] + 1 if row else None
        return next_id

    def __get_next_card_id(self):
        row = self.__read_single('SELECT COALESCE(MAX(id),0) AS max_id FROM "CreditCards"')
        next_id = row['max_id'] + 1 if row else None
        return next_id

    # If all the validations are successful then the OrderService should reserve the product, store it in
    # the database, send an event that the order has been created and return 201 HTTP Status Code
    # með order id-i sem response message.
    def create_order(self, order: OrderInputModel):
        create_card_execution_string = '''
            INSERT INTO "CreditCards" (id, "cardNumber", "expirationMonth", "expirationYear", cvc)
            VALUES (%s, %s, %s, %s, %s) RETURNING *
        '''
        params = (self.__get_next_card_id(), order.credit_card.card_number, order.credit_card.expiration_month, order.credit_card.expiration_year, order.credit_card.cvc)
        card_row = self.__write_returning(create_card_execution_string, params)

        new_card_id = card_row['id'] if card_row else None
        if not new_card_id: return None

        create_order_execution_string = '''
            INSERT INTO Orders (id, "productId", "merchantId", "buyerId", "creditCardId", discount)
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING *
        '''
        params = (self.__get_next_order_id(), order.product_id, order.merchant_id, order.buyer_id, new_card_id, order.discount)
        order_row = self.__write_returning(create_order_execution_string, params)

        if not order_row: return None

        return {
            'id': order_row['id'],
            Order.PRODUCT_ID.value: order_row[Order.PRODUCT_ID.value],
            Order.MERCHANT_ID.value: order_row[Order.MERCHANT_ID.value],
            Order.BUYER_ID.value: order_row[Order.BUYER_ID.value],
            Order.CREDIT_CARD.value: {
                CreditCard.CARD_NUMBER.value: card_row[CreditCard.CARD_NUMBER.value],
                CreditCard.EXPIRATION_MONTH.value: card_row[CreditCard.EXPIRATION_MONTH.value],
                CreditCard.EXPIRATION_YEAR.value: card_row[CreditCard.EXPIRATION_YEAR.value],
                CreditCard.CVC.value: card_row[CreditCard.CVC.value]
            },
            Order.DISCOUNT.value: float(order_row[Order.DISCOUNT.value])
        }



