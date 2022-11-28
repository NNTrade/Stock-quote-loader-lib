from ..abs_stock_quote_loader import AbsStockQuoteLoader, TimeFrame, date, pd, URL
from abc import ABC, abstractmethod, abstractproperty
from .inveting_com_loader import load_stock_candles
from .stock import InvestingStock

class InvestingStockQuoteLoader(AbsStockQuoteLoader):

    def download(self, stock, date_from:date, date_till:date, timeframe: TimeFrame)->pd.DataFrame:
        if not isinstance(stock, InvestingStock):
            raise AttributeError("Stock must be instance of InvestingStock")
        return load_stock_candles(stock.Stock, stock.Country, date_from, date_till, timeframe)
    
    @property
    def source_url(self)->URL:
        return URL("https://www.investing.com/")