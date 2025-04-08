import os
import sys
import pymongo
import certifi
from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY
from dotenv import load_dotenv

load_dotenv()

class MongoDBClient:
    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                
                if not mongo_db_url:
                    raise Exception(f"Environment variable '{MONGODB_URL_KEY}' is not set.")
                
                MongoDBClient.client = pymongo.MongoClient(
                    mongo_db_url,
                    tls=True,
                    tlsCAFile=certifi.where()
                )

                MongoDBClient.client.admin.command('ping')
                logging.info("MongoDB connection established successfully")
            
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            logging.error(f"MongoDB connection failed: {str(e)}")
            raise MyException(e, sys)

    def __getitem__(self, collection_name: str):
        """Enable square bracket notation to access collections"""
        return self.database[collection_name]