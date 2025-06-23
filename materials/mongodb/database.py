# Iosif Vieru 1409A
# 14.11.2024

import pymongo
from sys import exit
import dotenv, os

dotenv.load_dotenv()

MONGO_DB_USER = os.getenv("MONGO_DB_USER")
MONGO_DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
MONGO_DB_HOST = os.getenv("MONGO_DB_HOST")
MONGO_DB_PORT = int(os.getenv("MONGO_DB_PORT"))

try:
    mongodb_uri = f"mongodb://{MONGO_DB_USER}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOST}:{MONGO_DB_PORT}"
    client = pymongo.MongoClient(mongodb_uri)
    db = client["materiale"]
    collection = db["materiale_database"]
except Exception as e:
    print("[Database]", e)
    exit(1)