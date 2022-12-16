from .abs_cache import AbsCache, pd, date, TimeFrame
import os
import logging


class FileCache(AbsCache):
  def __init__(self, cache_folder: str):
      self.__cache_folder = cache_folder
      self.logger = logging.getLogger("FileCacheLoader")

  def save_df(self, df: pd.DataFrame, source:str, stock, date_from: date, date_till: date, timeframe: TimeFrame)->str:
    cache_path = self.__cache_file_path__(source, stock, date_from, date_till, timeframe) 
    if os.path.exists(cache_path):   
      self.logger.info("Remove previous cached file %s", cache_path)    
      os.remove(cache_path)

    df.to_csv(cache_path, sep=";",decimal=",")
    self.logger.info("Save df into file %s", cache_path)    
    return cache_path

  def load_df(self, source:str, stock, date_from: date, date_till: date, timeframe: TimeFrame) -> pd.DataFrame:
    cache_path = self.__cache_file_path__(source, stock, date_from, date_till, timeframe)
    if not os.path.exists(cache_path):   
      return None
    df = pd.read_csv(cache_path,sep=";", decimal=",").set_index("start_date_time")
    self.logger.info("Load df from file %s", cache_path)    
    return df

  def __cache_file_path__(self,source:str, stock, date_from: date, date_till: date, timeframe: TimeFrame ):
    return os.path.join(self.__cache_folder, FileCache.args_to_file_name(source, stock, date_from, date_till, timeframe)) 

  @staticmethod
  def args_to_file_name(source:str, stock, date_from: date, date_till: date, timeframe: TimeFrame) ->str:
    date_from_str = date_from.strftime('%Y-%m-%d')
    date_till_str = date_till.strftime('%Y-%m-%d')
    return f'{source}__{stock}__{date_from_str}__{date_till_str}__{timeframe.full_name()}.csv'