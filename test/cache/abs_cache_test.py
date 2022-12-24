import unittest
import logging
from NNTrade.common import TimeFrame
from src.cache import FileCache, MongoCache, AbsCache
from src.config import QuoteRequest, ChartConfig, LoadRequest,Source
from src.loader import YahooStockQuoteLoader
from datetime import date
from test.test_tools.compare_dt import compare_df

def get_impl_dic():
    return {
      "FileCache": FileCache("./output_files"),
      "MongoCache": MongoCache("192.168.100.227")
    }

class AbsCacheImpl_TestCase(unittest.TestCase):


    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    impl_dic = get_impl_dic()


    def test_WHEN_get_data_from_cache_THEN_get_same_data(self):
      # Array
      expected_request = QuoteRequest(ChartConfig("EURUSD=X",TimeFrame.D), date(2020,2,3), date(2020,2,6))
      expected_df = YahooStockQuoteLoader().download(expected_request)
      expected_load_request = LoadRequest(Source.Yahoo, expected_request)
      self.logger.info("Expected df")
      self.logger.info(expected_df)
      
      for i in self.impl_dic:
        with self.subTest(i=i):
          impl_name = i
          impl: AbsCache = self.impl_dic[i]
          
          # Act
          self.logger.info(f"Test {impl_name}")
          YahooStockQuoteLoader(impl).download(expected_request, reload_cache=True)
          asserted_df = impl.load_df(expected_load_request)
          
          # Assert
          self.logger.info("Asserted df")
          self.logger.info(asserted_df)
          compare_df(self, expected_df, asserted_df)
