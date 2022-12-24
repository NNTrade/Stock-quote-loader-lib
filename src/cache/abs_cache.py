from abc import ABC, abstractmethod
import pandas as pd
from ..config import LoadRequest

class AbsCache(ABC):
  @abstractmethod
  def save_df(self, df:pd.DataFrame, load_request: LoadRequest):
    ...
 
  @abstractmethod
  def load_df(self, load_request: LoadRequest)->pd.DataFrame:
    ...
    
  @abstractmethod
  def args_to_key(self, load_request: LoadRequest):
    ...