import psycopg2
import psycopg2.extras
from db_config import DbConfig


class Repository:

    def __init__(self):
        self.__db_config = DbConfig(
            user='postgres',
            password='postgres',
            database='Payments',
            host='payment-service-db'
        )

        self.__write('''
         CREATE TABLE IF NOT EXISTS Payments
         (
             id                INTEGER PRIMARY KEY,
             "orderId"         INTEGER NOT NULL,
             "paymentResult"   TEXT
         )
         ''')

    def __get_connection(self):
        return psycopg2.connect(
            user = self.__db_config.user,
            password = self.__db_config.password,
            database = self.__db_config.database,
            host = self.__db_config.host
        )

    def __write(self, execution_string, params=None):
        connection = self.__get_connection()
        cursor = connection.cursor()

        cursor.execute(execution_string, params) if params else cursor.execute(execution_string)
        connection.commit()

        cursor.close()
        connection.close()


    def __read_single(self, execution_string, params=None):
        connection = self.__get_connection()
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cursor.execute(execution_string, params) if params else cursor.execute(execution_string)
        row = cursor.fetchone()

        cursor.close()
        connection.close()
        return row


    def __get_next_id(self):
        row = self.__read_single("SELECT COALESCE(MAX(id),0) AS max_id FROM Payments")
        next_id = row['max_id'] + 1 if row else None
        return next_id


    def create_payment_result(self, order_id, result):
        execution_string = '''
            INSERT INTO Payments (id, "orderId", "paymentResult") 
            VALUES (%s, %s, %s)
        '''
        self.__write(execution_string, (self.__get_next_id(), order_id, result))



