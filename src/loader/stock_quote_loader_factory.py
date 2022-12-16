from . import YahooStockQuoteLoader, MoexStockQuoteLoader, AbsStockQuoteLoader

def get_yahoo_loader()->AbsStockQuoteLoader:
  return YahooStockQuoteLoader()

def get_moex_loader()->AbsStockQuoteLoader:
  return MoexStockQuoteLoader()