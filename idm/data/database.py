# Iosif Vieru 5.12.2024
# 1409A

from peewee import MySQLDatabase
from sys import exit
import dotenv, os

dotenv.load_dotenv()

IDM_MYSQL_DATABASE = os.getenv("IDM_MYSQL_DATABASE")
IDM_MYSQL_USER = os.getenv("IDM_MYSQL_USER")
IDM_MYSQL_PASSWORD = os.getenv("IDM_MYSQL_PASSWORD")
IDM_MYSQL_HOST = os.getenv("IDM_MYSQL_HOST")
IDM_MYSQL_PORT = int(os.getenv("IDM_MYSQL_PORT"))

try:
    db = MySQLDatabase(
        database=IDM_MYSQL_DATABASE,
        user=IDM_MYSQL_USER,
        password=IDM_MYSQL_PASSWORD,
        host=IDM_MYSQL_HOST,
        port=IDM_MYSQL_PORT
    )

except Exception as e:
    print("[DB] Error: ", e)
    exit(1)
