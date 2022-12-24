from abc import ABC, abstractmethod, abstractproperty
from httpx import URL
import pandas as pd
from typing import List, Dict, Any
import logging
from ..cache import AbsCache
from ..config import QuoteRequest, Source, LoadRequest


class AbsStockQuoteLoader(ABC):

    def __init__(self, cache_loader: AbsCache = None) -> None:
        super().__init__()
        self.cache_loader = cache_loader
        self.logger = logging.getLogger("AbsStockQuoteLoader")

    @abstractmethod
    def _download_(self, quote_request: QuoteRequest) -> pd.DataFrame:
        ...
    @property
    @abstractproperty
    def source_type(self) -> Source:
        ...

    def download(self, quote_request: QuoteRequest, use_cache: bool = True, reload_cache: bool = False) -> pd.DataFrame:
        if use_cache and not reload_cache:
            if self.cache_loader is None:
                self.logger.warning(
                    "use_cache is True, but cache_logger is None")
            elif not reload_cache:
                cached_df = self.cache_loader.load_df(LoadRequest(self.source_type, quote_request))
                if cached_df is not None:
                    self.logger.info("Cached data found")
                    return cached_df
                self.logger.info("No cached data")

        loaded_df = self._download_(quote_request)

        if use_cache and self.cache_loader is not None:
            self.logger.info("Save df into cache")
            self.cache_loader.save_df(
                loaded_df, LoadRequest(self.source_type, quote_request))

        return loaded_df

    def download_many(self, quote_request_list: List[QuoteRequest]) -> Dict[Any, pd.DataFrame]:
        if not isinstance(quote_request_list, List):
            raise AttributeError("Stock should be a list")

        _ret_dic = {}
        for quote_request in quote_request_list:
            _ret_dic[quote_request] = self.download(quote_request)

        return _ret_dic

    @property
    @abstractproperty
    def source_url(self) -> URL:
        ...
