import psycopg2

import os
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv('DATABASE_HOST')
DB_NAME = os.getenv('DATABASE_NAME')
DB_USER = os.getenv('DATABASE_USERNAME')
DB_PASSWORD = os.getenv('DATABASE_PASSWORD')

class Database:
    def __init__(self):
        self.host = DB_HOST
        self.database = DB_NAME
        self.user = DB_USER
        self.password = DB_PASSWORD
        self.conn = None

    def connect(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
        )
        self.cur = self.conn.cursor()

    def disconnect(self):
        self.cur.close()
        self.conn.close()