import unittest
import logging
from datetime import date, timedelta
from NNTrade.common import TimeFrame
from src import YahooStockQuoteLoader, AbsStockQuoteLoader, InvestingStockQuoteLoader, InvestingStock, MoexStockQuoteLoader

class AbsStockQuoteLoaderImplTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    impl_dic = {"Yahoo": YahooStockQuoteLoader(), "Investing.com": InvestingStockQuoteLoader(), "Moex.ru": MoexStockQuoteLoader()}
    stock_source_map = {"Yahoo": "BTC-USD", "Investing.com": InvestingStock("AAPL", "United States"), "Moex.ru": "AAPL-RM"}


    expected_from_dt = date(2020, 9, 15)
    expected_till_dt = date(2020, 9, 18)

    def test_WHEN_request_source_url_THEN_get_url(self):
        # Array

        # Act
        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]
                self.logger.info(f"Test {impl_name}")
                self.assertIsNotNone(impl.source_url)  
    
    def test_WHEN_request_data_for_serveral_days_THEN_get_correct_count_of_lines(self):
        # Array
        expected_timeframe = TimeFrame.DAY

        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]
                expected_stock_code  = self.stock_source_map[i]

                self.logger.info(f"Test {impl_name}")

                # Act
                asserted_df = impl.download(expected_stock_code, self.expected_from_dt, self.expected_till_dt, expected_timeframe)
                
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

                # Act
                asserted_df = impl.download(expected_stock_code, self.expected_from_dt, self.expected_till_dt, expected_timeframe)
                
                # Assert
                self.logger.info("Loaded data")
                self.logger.info(asserted_df)
                self.assertEqual(5, len(asserted_df.columns))
                self.assertIn("open", asserted_df.columns)
                self.assertIn("high", asserted_df.columns)
                self.assertIn("low", asserted_df.columns)
                self.assertIn("close", asserted_df.columns)
                self.assertIn("volume", asserted_df.columns)

    def test_WHEN_request_data_THEN_get_correct_index_name(self):
        # Array
        expected_timeframe = TimeFrame.DAY

        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]
                expected_stock_code  = self.stock_source_map[i]

                self.logger.info(f"Test {impl_name}")

                # Act
                asserted_df = impl.download(expected_stock_code, self.expected_from_dt, self.expected_till_dt, expected_timeframe)
                
                # Assert
                self.logger.info("Loaded data")
                self.logger.info(asserted_df)
                self.assertEqual("start_date_time", asserted_df.index.name)

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

                # Act
                asserted_df = impl.download(expected_stock_code, self.expected_from_dt, expected_till_dt, expected_timeframe)
                
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

                # Assert
                with self.assertRaises(Exception):
                    impl.download(expected_stock_code, self.expected_from_dt, expected_till_dt, expected_timeframe)


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

                # Assert
                with self.assertRaises(Exception):
                    impl.download(expected_stock_code, self.expected_from_dt, expected_till_dt, expected_timeframe)
                    
    def test_WHEN_request_with_wrong_stock_THEN_get_exception(self):
        # Array
        expected_stock_code = "BTC-USDsdsdsds"
        expected_timeframe = TimeFrame.DAY

        for i in self.impl_dic:
            with self.subTest(i=i):
                impl_name = i
                impl: AbsStockQuoteLoader = self.impl_dic[i]

                self.logger.info(f"Test {impl_name}")

                # Assert
                with self.assertRaises(Exception):
                    impl.download(expected_stock_code, self.expected_from_dt, self.expected_till_dt, expected_timeframe)

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
                        with self.assertRaises(Exception):
                            impl.download(expected_stock_code, self.expected_from_dt, expected_till_dt, i)