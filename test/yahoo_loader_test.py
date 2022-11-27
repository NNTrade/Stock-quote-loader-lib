import unittest
import logging
import pandas as pd
from datetime import datetime, date
from src import load_stock_candles
from NNTrade.common import TimeFrame
from test.test_tools.compare_dt import compare_df


class LoadQuoteTestCase(unittest.TestCase):
    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(asctime)s %(module)s %(levelname)s: %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)

    def test_When_request_data_Then_get_correct_data(self):
        # Array
        expected_df = pd.DataFrame(data={"open": [8760.285156, 9078.308594, 9121.600586],
                                         "high": [9142.054688, 9167.695312, 9163.220703],
                                         "low": [8757.253906, 9032.079102, 8890.744141],
                                         "close": [9078.762695, 9122.545898, 8909.954102],
                                         "volume": [39698054597, 40826885651, 36216930370],
                                         "start_date_time": [datetime(2020, 3, 5), datetime(2020, 3, 6),
                                                             datetime(2020, 3, 7)]})\
                        .set_index("start_date_time")

        expected_stock_code = "BTC-USD"
        expected_timeframe = TimeFrame.DAY
        expected_from_dt = date(2020, 3, 5)
        expected_till_dt = date(2020, 3, 8)

        # Act
        asserted_df = load_stock_candles(expected_stock_code, expected_from_dt, expected_till_dt, expected_timeframe).round(6)

        # Assert
        self.logger.info("Loaded data")
        self.logger.info(asserted_df)
        compare_df(self, expected_df, asserted_df)

    def test_When_request_one_day_data_Then_get_correct_data(self):
        # Array
        expected_df = pd.DataFrame(data={"open": [8760.285156],
                                         "high": [9142.054688],
                                         "low": [8757.253906],
                                         "close": [9078.762695],
                                         "volume": [39698054597],
                                         "start_date_time": [datetime(2020, 3, 5)]})\
                        .set_index("start_date_time")

        expected_stock_code = "BTC-USD"
        expected_timeframe = TimeFrame.DAY
        expected_from_dt = date(2020, 3, 5)
        expected_till_dt = date(2020, 3, 6)

        # Act
        asserted_df = load_stock_candles(expected_stock_code, expected_from_dt, expected_till_dt, expected_timeframe).round(6)

        # Assert
        self.logger.info("Loaded data")
        self.logger.info(asserted_df)
        compare_df(self, expected_df, asserted_df)

    def test_When_request_till_less_from_Then_get_error(self):
        # Array
        expected_stock_code = "BTC-USD"
        expected_timeframe = TimeFrame.DAY
        expected_from_dt = date(2020, 3, 5)
        expected_till_dt = date(2020, 3, 4)

        # Assert
        with self.assertRaises(Exception):
            load_stock_candles(expected_stock_code, expected_from_dt, expected_till_dt, expected_timeframe)


    def test_When_request_till_eq_from_Then_get_error(self):
        # Array
        expected_stock_code = "BTC-USD"
        expected_timeframe = TimeFrame.DAY
        expected_from_dt = date(2020, 3, 5)
        expected_till_dt = date(2020, 3, 5)

        # Assert
        with self.assertRaises(Exception):
            load_stock_candles(expected_stock_code, expected_from_dt, expected_till_dt, expected_timeframe)

    def test_WHEN_request_with_wrong_stock_THEN_get_exception(self):
        # Array
        expected_stock_code = "BTC-USDsdsdsds"
        expected_timeframe = TimeFrame.DAY
        expected_from_dt = date(2020, 3, 5)
        expected_till_dt = date(2020, 3, 6)

        expected_df = pd.DataFrame(data={"open": [],
                                         "high": [],
                                         "low": [],
                                         "close": [],
                                         "volume": [],
                                         "start_date_time": []}) \
            .set_index("start_date_time")

        # Act
        asserted_df = load_stock_candles(expected_stock_code, expected_from_dt, expected_till_dt, expected_timeframe)

        # Assert
        self.logger.info("Loaded data")
        self.logger.info(asserted_df)
        compare_df(self, expected_df, asserted_df)

    def test_WHEN_request_more_than_30_intraday_THEN_get_exception(self):
        # Array
        expected_stock_code = "BTC-USD"
        expected_from_dt = date(2020, 3, 5)
        expected_till_dt = date(2020, 4, 6)

        # Assert
        for i in [e for e in TimeFrame if e.to_seconds() < 24*60*60]:
            with self.subTest(i=i):
                with self.assertRaises(Exception):
                    load_stock_candles(expected_stock_code, expected_from_dt, expected_till_dt, i)
