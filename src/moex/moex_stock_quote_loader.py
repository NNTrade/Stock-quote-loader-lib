from ..abs_stock_quote_loader import AbsStockQuoteLoader, TimeFrame, date, pd, URL
from abc import ABC, abstractmethod, abstractproperty
import logging
from ..date_checks import check_date
import pandas_datareader as pdr
from datetime import timedelta

class MoexStockQuoteLoader(AbsStockQuoteLoader):

    def download(self, stock, date_from:date, date_till:date, timeframe: TimeFrame)->pd.DataFrame:
       
        logger: logging.Logger = logging.getLogger("func yahoo_loader.load_stock_candles")
        logger.debug("Check input parameters")
        
        check_date(date_from, date_till)

        if timeframe != TimeFrame.DAY:
          raise AttributeError(
                    f"Moex loader support only Timeframe.Day")

        if timeframe.to_seconds() < 24*60*60:
            if (date_till - date_from).days > 30:
                raise AttributeError(
                    f"For intraday stock quote allows only 30 days")


        logger.info("Start download from MOEX finance")
        from_date = date_from.strftime('%Y-%m-%d')
        till_date = (date_till - timedelta(days=1)).strftime('%Y-%m-%d')

        logger.info(
            f"Download stock {stock} timeframe {timeframe.name}")
        data: pd.DataFrame = pdr.get_data_moex([stock], from_date, till_date)

        data = data[["OPEN", "LOW","HIGH","CLOSE","VOLUME"]]
        data.columns = [c.lower() for c in data.columns]
        data.index = data.index.rename('start_date_time')

        if len(data) == 0:
            raise AttributeError(
                    f"No data for stock {stock}")

        return data
    
    @property
    def source_url(self)->URL:
        return URL("https://www.moex.com/")