# Stock quote loader

## Import
```python
from NNTrade.datasource.stock_quote_loader_lib.loader import YahooStockQuoteLoader,date, TimeFrame
from NNTrade.datasource.stock_quote_loader_lib.cache import FileCache

sql = YahooStockQuoteLoader(FileCache("./cached_stock/"))
```

## Intall
NNTrade.datasource.stock_quote_loader_lib @ git+https://git@github.com/NNTrade/Stock-quote-loader-lib.git#egg=NNTrade.datasource.stock_quote_loader_lib