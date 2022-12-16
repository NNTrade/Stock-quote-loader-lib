from abc import ABC, abstractmethod, abstractproperty
from datetime import date
from httpx import URL
import pandas as pd
from NNTrade.common import TimeFrame
from typing import List, Dict, Any
import logging
from ..cache import AbsCache


class AbsStockQuoteLoader(ABC):

    def __init__(self, cache_loader: AbsCache = None) -> None:
        super().__init__()
        self.cache_loader = cache_loader
        self.logger = logging.getLogger("AbsStockQuoteLoader")

    @abstractmethod
    def _download_(self, stock, date_from: date, date_till: date, timeframe: TimeFrame) -> pd.DataFrame:
        ...

    def download(self, stock, date_from: date, date_till: date, timeframe: TimeFrame, use_cache: bool = True, reload_cache: bool = False) -> pd.DataFrame:
        if use_cache and not reload_cache:
            if self.cache_loader is None:
                self.logger.warning(
                    "use_cache is True, but cache_logger is None")
            elif not reload_cache:
                cached_df = self.cache_loader.load_df(
                    self.__class__.__name__, stock, date_from, date_till, timeframe)
                if cached_df is not None:
                    self.logger.info("Cached data found")
                    return cached_df
                self.logger.info("No cached data")

        loaded_df = self._download_(stock, date_from, date_till, timeframe)

        if use_cache and self.cache_loader is not None:
            self.logger.info("Save df into cache")
            self.cache_loader.save_df(
                loaded_df, self.__class__.__name__, stock, date_from, date_till, timeframe)

        return loaded_df

    def download_many(self, stock_list: List, date_from: date, date_till: date, timeframe: TimeFrame) -> Dict[Any, pd.DataFrame]:
        if not isinstance(stock_list, List):
            raise AttributeError("Stock should be a list")

        _ret_dic = {}
        for stock in stock_list:
            _ret_dic[stock] = self.download(
                stock, date_from, date_till, timeframe)

        return _ret_dic

    @property
    @abstractproperty
    def source_url(self) -> URL:
        ...
