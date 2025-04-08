import os
import pandas as pd
import numpy as np
from typing import Optional
import sys
import certifi
from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME
from src.configuration.mongo_db_connection import MongoDBClient

ca = certifi.where()

class Data:
    mongo_client = None 

    def __init__(self) -> None:
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)
        
    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]
            
            doc_count = collection.count_documents({})
            
            if doc_count == 0:
                return pd.DataFrame()
            
            cursor = collection.find()
            documents = list(cursor)
            
            df = pd.DataFrame(documents)
            
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)
            elif "id" in df.columns:
                df.drop(columns=["id"], inplace=True)
            
            df.replace({"na": np.nan}, inplace=True)
            
            return df
        except Exception as e:
            raise MyException(e, sys)