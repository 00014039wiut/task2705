import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

dbname = 'new_db'
user = "postgres"
host = "localhost"
password = "Sql7575"
port = 5432

db_params = {
    'database': os.getenv('database'),
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'port': os.getenv('port'),
}


class DBManager:
    def __init__(self, db_params: dict):
        self.db_params = db_params

    def __enter__(self):
        self.conn = psycopg2.connect(**self.db_params)
        self.cur = self.conn.cursor()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        if self.conn:
            self.cur.close()
            self.conn.close()

    def commit(self):
        self.conn.commit()


class Product:

    def insert_product(self):
        name1 = input("Enter name : ")
        price1 = input("Enter price : ")
        country1 = input("Enter country : ")
        with DBManager(db_params) as manager:
            try:
                insert_query = """INSERT INTO product(name, price, country) VALUES(%s, %s, %s)"""
                manager.cur.execute(insert_query, (name1, price1, country1))
                manager.commit()
                print("Product inserted successfully.")
            except psycopg2.Error as e:
                print(f"An error occurred: {e}")
                manager.conn.rollback()


product = Product()
product.insert_product()
