# Stock-quote-loader-lib
Service for loading Stock quotes

## Install
NNTrade.datasource.stock_quote_loader_lib @ git+https://git@github.com/NNTrade/Stock-quote-loader-lib.git#egg=NNTrade.datasource.stock_quote_loader_lib

## Use
```python
from NNTrade.datasource.stock_quote_loader_lib.loader import YahooStockQuoteLoader,date, TimeFrame
from NNTrade.datasource.stock_quote_loader_lib.cache import FileCache

sql = YahooStockQuoteLoader(FileCache("./cached_stock/"))

sql.download("AAPL", date(2010,1,1), date(2020,1,1), TimeFrame.D)
```

## Option
NNTrade.datasource.stock_quote_loader_lib.cache.AbsCache - abstract class for cache data
NNTrade.datasource.stock_quote_loader_lib.cache.FileCache - realization of AbsCache to store data in files

from NNTrade.datasource.stock_quote_loader_lib.loader
- AbsStockQuoteLoader - abstract class for load data
- YahooStockQuoteLoader - download data from Yahoo finace
- MoexStockQuoteLoader - download data from Moex