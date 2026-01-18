import os
from BuyerService.models.buyer_input_model import BuyerModel
import sqlite3

#   buyer-services:
    # volumes:
    #   - ./BuyerService:/app/BuyerService

class BuyerRepositorySQLight:

    def __init__(self):
        db_path = r'sqlite_data/buyer_database.db'
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute('''
       CREATE TABLE IF NOT EXISTS Buyers 
       (id INTEGER PRIMARY KEY, 
        name TEXT, 
        ssn TEXT, 
        email TEXT, 
        phone_number TEXT)
       ''')
        connection.close()

    def get_buyer_by_id(self, buyer_id):
        connection = sqlite3.connect('sqlite_data/buyer_database.db')
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Buyers WHERE id = ?", (buyer_id,))
        row = cursor.fetchone()
        connection.close()
        return row

    def create_buyer(self, buyer: BuyerModel):
        db_path = r'sqlite_data/buyer_database.db'
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(
            '''
            INSERT INTO Buyers(name, ssn, email, phone_number)
            VALUES (?, ?, ?, ?)
            ''',
            (buyer.name, buyer.ssn, buyer.email, buyer.phone_number)
        )
        cursor.close()
        connection.commit()
        connection.close()

        return {'msg': 'Buyer created successfully', 'status': 200}







