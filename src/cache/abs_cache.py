from abc import ABC, abstractmethod
from datetime import date
import pandas as pd
from NNTrade.common import TimeFrame

class AbsCache(ABC):
  @abstractmethod
  def save_df(self, df:pd.DataFrame, source:str, stock, date_from: date, date_till: date, timeframe: TimeFrame):
    ...
  
  @abstractmethod
  def load_df(self, source:str, stock, date_from:date, date_till:date, timeframe: TimeFrame)->pd.DataFrame:
    ...