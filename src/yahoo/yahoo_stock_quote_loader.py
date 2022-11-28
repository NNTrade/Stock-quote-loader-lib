from ..abs_stock_quote_loader import AbsStockQuoteLoader, TimeFrame, date, pd, URL
from abc import ABC, abstractmethod, abstractproperty
from .yahoo_loader import load_stock_candles

class YahooStockQuoteLoader(AbsStockQuoteLoader):

    def download(self, stock, date_from:date, date_till:date, timeframe: TimeFrame)->pd.DataFrame:
        return load_stock_candles(stock, date_from, date_till, timeframe)
    
    @property
    def source_url(self)->URL:
        return URL("https://finance.yahoo.com/")