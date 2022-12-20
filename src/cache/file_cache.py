from .abs_cache import AbsCache, pd
import os
import logging
from ..loader.config import LoadRequest

class FileCache(AbsCache):
  def __init__(self, cache_folder: str):
      self.__cache_folder = cache_folder
      self.logger = logging.getLogger("FileCache")

  def save_df(self, df: pd.DataFrame, load_request: LoadRequest)->str:
    cache_path = self.__cache_file_path__(load_request) 
    if os.path.exists(cache_path):   
      self.logger.info("Remove previous cached file %s", cache_path)    
      os.remove(cache_path)

    df.to_csv(cache_path, sep=";",decimal=",")
    self.logger.info("Save df into file %s", cache_path)    
    return cache_path

  def load_df(self, load_request: LoadRequest) -> pd.DataFrame:
    cache_path = self.__cache_file_path__(load_request)
    if not os.path.exists(cache_path):   
      return None
    df = pd.read_csv(cache_path,sep=";", decimal=",").set_index("start_date_time")
    self.logger.info("Load df from file %s", cache_path)    
    return df

  def __cache_file_path__(self,load_request: LoadRequest):
    return os.path.join(self.__cache_folder, self.args_to_key(load_request)) 

  def args_to_key(self, load_request: LoadRequest):
    date_from_str = load_request.quote_request.date_from.strftime('%Y-%m-%d')
    date_till_str = load_request.quote_request.date_till.strftime('%Y-%m-%d')
    return f'{load_request.source.value}__{load_request.quote_request.chart.stock}__{load_request.quote_request.chart.timeframe.full_name()}__{date_from_str}__{date_till_str}.csv'