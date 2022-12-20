from .abs_cache import AbsCache, pd
import logging
from ..loader.config import LoadRequest
from typing import Tuple
from pymongo import MongoClient
from pymongo.collection import Collection
import io

class MongoCache(AbsCache):
  def __init__(self, mongo_host: str, mongo_port:int = 27017, mongo_user: str = "quote", mongo_pswd:str = "quote", authSource:str = "users", database:str="quote"):
      self.logger = logging.getLogger("MongoCache")
      self.__mongo_host = mongo_host
      self.__mongo_port = mongo_port
      self.__mongo_user = mongo_user
      self.__mongo_pswd = mongo_pswd
      self.__mongo_authSource = authSource
      self.__mongo_database = database

  def __create_connection__(self, collection_name: str) -> Tuple[MongoClient, Collection]:
    self.logger.info(
        "Open connection to host: %s DB: %s collection: %s", self.__mongo_host, self.__mongo_database,collection_name )
    mng_client = MongoClient(
        host=self.__mongo_host,
        port=self.__mongo_port,
        username=self.__mongo_user,
        password=self.__mongo_pswd,
        authSource=self.__mongo_authSource)
    mng_db = mng_client[self.__mongo_database]
    mng_collection = mng_db[collection_name]
    return mng_client, mng_collection

  def save_df(self, df: pd.DataFrame, load_request: LoadRequest)->str:
    csv_str = df.to_csv(sep=";",decimal=",")
    try:
      mng_client, mng_collection = self.__create_connection__(load_request.source.name)

      data = {}
      data["query_request"] = self.args_to_key(load_request)
      data["payload"] = csv_str
      new_obj_id = mng_collection.insert_one(data)
      
      self.logger.info("Save df into new objectID %s", new_obj_id.inserted_id)    
      return new_obj_id
    finally:
      mng_client.close()
    
  def load_df(self, load_request: LoadRequest) -> pd.DataFrame:
    try:
      mng_client, mng_collection = self.__create_connection__(load_request.source.name)

      query = {}
      query["query_request"] = self.args_to_key(load_request)
      _ret = None
      for doc in mng_collection.find(query):
        if _ret is None:
          buffer = io.StringIO(doc["payload"])
          _ret = pd.read_csv(buffer ,sep=";", decimal=",").set_index("start_date_time")
        else:
          self.logger.warning("Find several cached data, clear manualy. Collection %s config %s", load_request.source.name, self.args_to_key())

      return _ret
    finally:
      mng_client.close()

  def args_to_key(self, load_request: LoadRequest):
    return load_request.quote_request.to_dict()