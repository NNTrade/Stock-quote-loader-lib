from typing import Any, Dict, List, Tuple
from ..abs_stock_quote_loader import AbsStockQuoteLoader, TimeFrame, date, pd, URL
from abc import ABC, abstractmethod, abstractproperty
import logging
from ..date_checks import check_date
import pandas_datareader as pdr
from datetime import timedelta

class MoexStockQuoteLoader(AbsStockQuoteLoader):
    logger = logging.getLogger("MoexStockQuoteLoader")

    def __check_input_parameters__(self, date_from:date, date_till:date, timeframe: TimeFrame):
        check_date(date_from, date_till)

        if timeframe != TimeFrame.DAY:
          raise AttributeError(
                    f"Moex loader support only Timeframe.Day")

        if timeframe.to_seconds() < 24*60*60:
            if (date_till - date_from).days > 30:
                raise AttributeError(
                    f"For intraday stock quote allows only 30 days")

    def __convert_date__(self,date_from:date, date_till:date )-> Tuple[date, date]:
        return date_from, (date_till - timedelta(days=1))

    def __convert_moex_df__(self, moex_df:pd.DataFrame)->pd.DataFrame:
        ret_df = moex_df[["OPEN", "LOW","HIGH","CLOSE","VOLUME"]]
        ret_df.columns = [c.lower() for c in ret_df.columns]
        ret_df.index = ret_df.index.rename('start_date_time')
        return ret_df

    def download(self, stock, date_from:date, date_till:date, timeframe: TimeFrame)->pd.DataFrame:
       
        logger: logging.Logger = self.logger.getChild("download")
        logger.debug("Check input parameters")
        self.__check_input_parameters__(date_from, date_till, timeframe)
        

        logger.info("Start download from MOEX finance")
        from_date, till_date = self.__convert_date__(date_from, date_till)

        logger.info(
            f"Download stock {stock} timeframe {timeframe.name}")
        data: pd.DataFrame = pdr.get_data_moex([stock], from_date, till_date)

        ret_data = self.__convert_moex_df__(data)

        if len(ret_data) == 0:
            raise AttributeError(
                    f"No data for stock {stock}")

        return ret_data
    
    '''
    Deprecated
    def download_many(self, stock_list: List, date_from: date, date_till: date, timeframe: TimeFrame) -> Dict[Any, pd.DataFrame]:
        logger: logging.Logger = self.logger.getChild("download_many")
        logger.debug("Check input parameters")
        self.__check_input_parameters__(date_from, date_till, timeframe)

        if not isinstance(stock_list, List):
            raise AttributeError("Stock should be a list")

        logger.info("Start download_many from MOEX finance")
        from_date, till_date = self.__convert_date__(date_from, date_till)

        logger.info(
            f"Download stock {stock_list} timeframe {timeframe.name}")

        data: pd.DataFrame = pdr.get_data_moex(stock_list, from_date, till_date)

        _ret_dic = {}
        for stock in stock_list:
            _ret_dic[stock] = self.__convert_moex_df__(data[data["SECID"]==stock])

        return _ret_dic
    '''

    @property
    def source_url(self)->URL:
        return URL("https://www.moex.com/")