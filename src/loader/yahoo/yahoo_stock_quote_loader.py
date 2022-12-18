from ..config import QuoteRequest, Source
from ..abs_stock_quote_loader import AbsStockQuoteLoader, TimeFrame, date, pd, URL
from .yahoo_loader import load_stock_candles

class YahooStockQuoteLoader(AbsStockQuoteLoader):

    def _download_(self, quote_request: QuoteRequest)->pd.DataFrame:
        return load_stock_candles(quote_request.chart.stock, quote_request.date_from, quote_request.date_till, quote_request.chart.timeframe)
    
    @property
    def source_url(self)->URL:
        return URL("https://finance.yahoo.com/")
    
    @property
    def source_type(self)->Source:
        return Source.Yahoo
