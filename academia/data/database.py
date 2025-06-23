# Iosif Vieru 1409A
# 24.10.2024

from peewee import MySQLDatabase
from sys import exit
import dotenv
import os

dotenv.load_dotenv()

MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))

try:
    db = MySQLDatabase(
        database=MYSQL_DATABASE,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        host=MYSQL_HOST,
        port=MYSQL_PORT
    )
    
except Exception as e:
    print("[DB] Error: ", e)
    exit(1)