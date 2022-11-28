from abc import ABC, abstractmethod, abstractproperty
from datetime import date
from httpx import URL
import pandas as pd
from NNTrade.common import TimeFrame
from typing import List, Dict, Any

class AbsStockQuoteLoader(ABC):

    @abstractmethod
    def download(self, stock, date_from:date, date_till:date, timeframe: TimeFrame)->pd.DataFrame:
        ...
    
    @abstractmethod
    def download_many(self, stock_list:List, date_from:date, date_till:date, timeframe: TimeFrame)->Dict[Any,pd.DataFrame]:
        if not isinstance(stock_list, List):
            raise AttributeError("Stock should be a list")

        _ret_dic = {}
        for stock in stock_list:
            _ret_dic[stock] = self.download(stock, date_from, date_till, timeframe)

        return _ret_dic

    @property
    @abstractproperty
    def source_url(self)->URL:
        ...