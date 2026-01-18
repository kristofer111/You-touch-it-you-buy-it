import psycopg2
import psycopg2.extras

from BuyerService.enums.buyer import Buyer
from BuyerService.models.buyer_input_model import BuyerInputModel


class BuyerRepository:

    def __init__(self, db_config):
        self.__db_config = db_config
        self.__write('''
           CREATE TABLE IF NOT EXISTS Buyers 
           (id INTEGER PRIMARY KEY, 
            name TEXT, 
            ssn TEXT, 
            email TEXT,
            "phoneNumber" TEXT)
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


    def get_buyer_by_id(self, buyer_id):
        execution_string = "SELECT * FROM Buyers WHERE id = %s"
        buyer = self.__read_single(execution_string, (buyer_id,))
        if not buyer: return None

        return {
            Buyer.NAME.value: buyer[Buyer.NAME.value],
            Buyer.SSN.value: buyer[Buyer.SSN.value],
            Buyer.EMAIL.value: buyer[Buyer.EMAIL.value],
            Buyer.PHONE_NUMBER.value: buyer[Buyer.PHONE_NUMBER.value],
        }
    

    def __get_next_id(self):
        row = self.__read_single("SELECT COALESCE(MAX(id),0) AS max_id FROM Buyers")
        max_id = row['max_id'] + 1 if row else None
        return max_id


    def create_buyer(self, buyer: BuyerInputModel):
        execution_string = '''
          INSERT INTO Buyers(id, name, ssn, email, "phoneNumber")
          VALUES (%s, %s, %s, %s, %s)
          RETURNING id
          '''
        params = (self.__get_next_id(), buyer.name, buyer.ssn, buyer.email, buyer.phone_number)
        row = self.__write_returning(execution_string, params)

        new_id = row['id'] if row else None

        return new_id







