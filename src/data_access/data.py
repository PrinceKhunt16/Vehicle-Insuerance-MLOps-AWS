import os
import pandas as pd
import numpy as np
from typing import Optional
import sys
import pymongo
import certifi
from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY

ca = certifi.where()

class Data:
    mongo_client = None 

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            if Data.mongo_client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    mongo_db_url = "mongodb://localhost:27017/"
                    logging.warning(f"Environment variable '{MONGODB_URL_KEY}' not set. Defaulting to local MongoDB.")

                use_cert = ca if "mongodb+srv" in mongo_db_url else None

                Data.mongo_client = pymongo.MongoClient(mongo_db_url, tlsCAFile=use_cert)

            self.mongo_client = Data.mongo_client
            self.database = self.mongo_client[database_name]
            self.database_name = database_name
            logging.info(f"Connected to MongoDB database: {database_name}")

        except Exception as e:
            raise MyException(e, sys)
        
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            
            if "id" in df.columns.to_list():
                df = df.drop(columns=["id"], axis=1)
            
            df.replace({"na":np.nan},inplace=True)
            
            return df
        except Exception as e:
            raise MyException(e, sys)