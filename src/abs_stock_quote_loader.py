from abc import ABC, abstractmethod, abstractproperty
from datetime import date
from httpx import URL
import pandas as pd
from NNTrade.common import TimeFrame

class AbsStockQuoteLoader(ABC):

    @abstractmethod
    def download(self, stock, date_from:date, date_till:date, timeframe: TimeFrame)->pd.DataFrame:
        ...
    
    @property
    @abstractproperty
    def source_url(self)->URL:
        ...