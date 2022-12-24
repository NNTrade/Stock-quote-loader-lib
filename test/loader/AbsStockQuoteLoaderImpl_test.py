import unittest
import logging
from datetime import date, timedelta
from NNTrade.common import TimeFrame
from NNTrade.common.candle_col_name import CLOSE, LOW, OPEN, HIGH, VOLUME, INDEX
from src.loader import YahooStockQuoteLoader, AbsStockQuoteLoader, MoexStockQuoteLoader
from src.config import QuoteRequest, ChartConfig
from datetime import datetime

def get_impl_dic():
    return {"Yahoo": YahooStockQuoteLoader(), "Moex.ru": MoexStockQuoteLoader()}

class AbsStockQuoteLoaderImpl_source_url_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    impl_dic = get_impl_dic()
    
    def test_WHEN_request_source_url_THEN_get_url(self):
        # Array

        # Act
        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]
                self.logger.info(f"Test {impl_name}")
                self.assertIsNotNone(impl.source_url)  


class AbsStockQuoteLoaderImpl_download_mass_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    impl_dic = get_impl_dic()
    stock_source_map = {"Yahoo": ["BTC-USD","RUB=X"], 
                        "Moex.ru": ["AAPL-RM", "GAZP"]}


    expected_from_dt = date(2020, 9, 15)
    expected_till_dt = date(2020, 9, 18)

    def test_WHEN_request_data_THEN_get_correct_keys_in_dictionsty(self):
        # Array
        expected_timeframe = TimeFrame.DAY

        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]
                expected_stock_codes  = self.stock_source_map[i]

                self.logger.info(f"Test {impl_name}")
                expected_requests = [QuoteRequest(ChartConfig(expected_stock_code, expected_timeframe), self.expected_from_dt, self.expected_till_dt) for expected_stock_code in expected_stock_codes]

                # Act
                asserted_dic = impl.download_many(expected_requests)
                
                # Assert
                self.logger.info("Loaded data")
                self.logger.info(asserted_dic)
                self.assertEqual(len(expected_stock_codes), len(asserted_dic))
                for expected_request in expected_requests:
                    self.assertEqual(3, len(asserted_dic[expected_request]))

class AbsStockQuoteLoaderImpl_download_TestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    impl_dic = get_impl_dic()
    stock_source_map = {"Yahoo": "BTC-USD", "Moex.ru": "AAPL-RM"}


    expected_from_dt = date(2020, 9, 15)
    expected_till_dt = date(2020, 9, 18)

    def test_WHEN_request_data_for_serveral_days_THEN_get_correct_count_of_lines(self):
        # Array
        expected_timeframe = TimeFrame.DAY

        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]
                expected_stock_code  = self.stock_source_map[i]

                self.logger.info(f"Test {impl_name}")
                expected_request = QuoteRequest(ChartConfig(expected_stock_code, expected_timeframe), self.expected_from_dt, self.expected_till_dt)
                
                # Act
                asserted_df = impl.download(expected_request)
                
                # Assert
                self.logger.info("Loaded data")
                self.logger.info(asserted_df)
                self.assertEqual(3, len(asserted_df))

    def test_WHEN_request_data_THEN_get_correct_columns(self):
        # Array
        expected_timeframe = TimeFrame.DAY

        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]
                expected_stock_code  = self.stock_source_map[i]

                self.logger.info(f"Test {impl_name}")
                expected_request = QuoteRequest(ChartConfig(expected_stock_code, expected_timeframe), self.expected_from_dt, self.expected_till_dt)

                # Act
                asserted_df = impl.download(expected_request)
                
                # Assert
                self.logger.info("Loaded data")
                self.logger.info(asserted_df)
                self.assertEqual(INDEX, asserted_df.index.name)
                self.assertEqual(5, len(asserted_df.columns))
                self.assertIn(OPEN, asserted_df.columns)
                self.assertIn(HIGH, asserted_df.columns)
                self.assertIn(LOW, asserted_df.columns)
                self.assertIn(CLOSE, asserted_df.columns)
                self.assertIn(VOLUME, asserted_df.columns)

    def test_WHEN_request_data_THEN_get_correct_index(self):
        # Array
        expected_timeframe = TimeFrame.DAY

        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]
                expected_stock_code  = self.stock_source_map[i]

                self.logger.info(f"Test {impl_name}")
                expected_request = QuoteRequest(ChartConfig(expected_stock_code, expected_timeframe), self.expected_from_dt, self.expected_till_dt)

                # Act
                asserted_df = impl.download(expected_request)
                
                # Assert
                self.logger.info("Loaded data")
                self.logger.info(asserted_df)
                self.assertEqual("start_date_time", asserted_df.index.name, "Wrong index name")
                for index in asserted_df.index:
                    self.assertIsInstance(index, datetime, "Wrong index value")
                    

    def test_WHEN_request_dataa_for_one_day_data_THEN_get_1_line(self):
        # Array
        expected_timeframe = TimeFrame.DAY
        expected_till_dt = self.expected_from_dt + timedelta(days=1)

        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]
                expected_stock_code  = self.stock_source_map[i]

                self.logger.info(f"Test {impl_name}")
                expected_request = QuoteRequest(ChartConfig(expected_stock_code, expected_timeframe), self.expected_from_dt, expected_till_dt)

                # Act
                asserted_df = impl.download(expected_request)
                
                # Assert
                self.logger.info("Loaded data")
                self.logger.info(asserted_df)
                self.assertEqual(1, len(asserted_df))

    def test_WHEN_request_till_less_from_THEN_get_error(self):
        # Array
        expected_timeframe = TimeFrame.DAY
        expected_till_dt = self.expected_from_dt - timedelta(days=1)

        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]
                expected_stock_code  = self.stock_source_map[i]

                self.logger.info(f"Test {impl_name}")
                expected_request = QuoteRequest(ChartConfig(expected_stock_code, expected_timeframe), self.expected_from_dt, expected_till_dt)

                # Assert
                with self.assertRaises(Exception):
                    impl.download(expected_request)


    def test_WHEN_request_till_eq_from_THEN_get_error(self):
        # Array
        expected_timeframe = TimeFrame.DAY
        expected_till_dt = self.expected_from_dt

        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]
                expected_stock_code  = self.stock_source_map[i]

                self.logger.info(f"Test {impl_name}")
                expected_request = QuoteRequest(ChartConfig(expected_stock_code, expected_timeframe), self.expected_from_dt, expected_till_dt)

                # Assert
                with self.assertRaises(Exception):
                    impl.download(expected_request)
                    
    def test_WHEN_request_with_wrong_stock_THEN_get_exception(self):
        # Array
        expected_stock_code = "BTC-USDsdsdsds"
        expected_timeframe = TimeFrame.DAY

        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]

                self.logger.info(f"Test {impl_name}")
                expected_request = QuoteRequest(ChartConfig(expected_stock_code, expected_timeframe), self.expected_from_dt, self.expected_till_dt)

                # Assert
                with self.assertRaises(Exception):
                    impl.download(expected_request)

    def test_WHEN_request_more_than_30_intraday_THEN_get_exception(self):
        # Array
        expected_till_dt = self.expected_from_dt + timedelta(days=31)

        # Assert
        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]
                expected_stock_code  = self.stock_source_map[i]

                self.logger.info(f"Test {impl_name}")
                
                for i in [e for e in TimeFrame if e.to_seconds() < 24*60*60]:
                    with self.subTest(i=i):
                        expected_request = QuoteRequest(ChartConfig(expected_stock_code, i), self.expected_from_dt, expected_till_dt)
                        with self.assertRaises(Exception):
                            impl.download(expected_request)