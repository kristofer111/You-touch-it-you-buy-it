import psycopg2
import psycopg2.extras
from InventoryService.models.product_input_model import ProductInputModel
from InventoryService.enums.product import Product


class ProductRepository:

    def __init__(self, db_config):
        self.__db_config = db_config
        self.__write('''
           CREATE TABLE IF NOT EXISTS Products 
           (id INTEGER PRIMARY KEY, 
            "merchantId" INTEGER, 
            "productName" TEXT,
            price DECIMAL, 
            quantity INTEGER,
            reserved INTEGER)
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


    def get_product_by_id(self, product_id):
        execution_string = "SELECT * FROM Products WHERE id = %s"
        product = self.__read_single(execution_string, (product_id,))

        if not product: return None

        return {
            Product.MERCHANT_ID.value: product[Product.MERCHANT_ID.value],
            Product.PRODUCT_NAME.value: product[Product.PRODUCT_NAME.value],
            Product.PRICE.value: float(product[Product.PRICE.value]),
            Product.QUANTITY.value: product[Product.QUANTITY.value],
            Product.RESERVED.value: product[Product.RESERVED.value]
        }
    

    def __get_next_id(self):
        row = self.__read_single("SELECT COALESCE(MAX(id),0) AS max_id FROM Products")
        max_id = row['max_id'] + 1 if row else None
        return max_id


    def create_product(self, product: ProductInputModel):
      execution_string = '''
          INSERT INTO Products(id, "merchantId", "productName", price, quantity, reserved)
          VALUES (%s, %s, %s, %s, %s, %s)
          RETURNING id
          '''
      params = (self.__get_next_id(), product.merchant_id, product.product_name, product.price, product.quantity, 0)
      row = self.__write_returning(execution_string, params)

      new_id = row['id'] if row else None

      return new_id


    def reserve_product_by_id(self, product_id):
        execution_string = '''
            UPDATE Products
            SET reserved = reserved + 1
            WHERE id = %s
        '''
        self.__write(execution_string, (product_id,))


    def stop_reserve_product_by_id(self, product_id):
        execution_string = '''
            UPDATE Products
            SET reserved = reserved - 1
            WHERE id = %s
        '''
        self.__write(execution_string, (product_id,))


    def decrease_product_by_id(self, product_id):
        execution_string = '''
            UPDATE Products
            SET reserved = reserved - 1,
            quantity = quantity - 1
            WHERE id = %s
        '''
        self.__write(execution_string, (product_id,))





