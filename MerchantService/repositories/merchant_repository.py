import psycopg2
import psycopg2.extras

from MerchantService.enums.merchant import Merchant
from MerchantService.models.merchant_input_model import MerchantInputModel


class MerchantRepository:

    def __init__(self, db_config):
        self.__db_config = db_config
        self.__write('''
           CREATE TABLE IF NOT EXISTS Merchants 
           (id INTEGER PRIMARY KEY, 
            name TEXT, 
            ssn TEXT, 
            email TEXT, 
            "phoneNumber" TEXT,
            "allowsDiscount" BOOLEAN)
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


    def get_merchant_by_id(self, merchant_id):
        execution_string = "SELECT * FROM Merchants WHERE id = %s"
        merchant = self.__read_single(execution_string, (merchant_id,))
        if not merchant: return None

        return {
            Merchant.NAME.value: merchant[Merchant.NAME.value],
            Merchant.SSN.value: merchant[Merchant.SSN.value],
            Merchant.EMAIL.value: merchant[Merchant.EMAIL.value],
            Merchant.PHONE_NUMBER.value: merchant[Merchant.PHONE_NUMBER.value],
            Merchant.ALLOWS_DISCOUNT.value: merchant[Merchant.ALLOWS_DISCOUNT.value],
        }
    

    def __get_next_id(self):
        row = self.__read_single("SELECT COALESCE(MAX(id),0) AS max_id FROM Merchants")
        max_id = row['max_id'] + 1 if row else None
        return max_id


    def create_merchant(self, merchant: MerchantInputModel):
      execution_string = '''
          INSERT INTO Merchants(id, name, ssn, email, "phoneNumber", "allowsDiscount")
          VALUES (%s, %s, %s, %s, %s, %s)
          RETURNING id
          '''
      params = (self.__get_next_id(), merchant.name, merchant.ssn, merchant.email, merchant.phone_number, merchant.allows_discount)
      row = self.__write_returning(execution_string, params)

      new_id = row['id'] if row else None

      return new_id







