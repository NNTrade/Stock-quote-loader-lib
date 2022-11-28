from typing import Any, Dict, List
from ..abs_stock_quote_loader import AbsStockQuoteLoader, TimeFrame, date, pd, URL
from abc import ABC, abstractmethod, abstractproperty
from .yahoo_loader import load_stock_candles

class YahooStockQuoteLoader(AbsStockQuoteLoader):

    def download(self, stock, date_from:date, date_till:date, timeframe: TimeFrame)->pd.DataFrame:
        return load_stock_candles(stock, date_from, date_till, timeframe)
    
    '''
    Deprecated
    def download_many(self, stock_list: List, date_from: date, date_till: date, timeframe: TimeFrame) -> Dict[Any, pd.DataFrame]:
        if not isinstance(stock_list, List):
            raise AttributeError("Stock should be a list")

        _ret_dic = {}
        for stock in stock_list:
            _ret_dic[stock] = self.download(stock, date_from, date_till, timeframe)

        return _ret_dic
    '''

    @property
    def source_url(self)->URL:
        return URL("https://finance.yahoo.com/")