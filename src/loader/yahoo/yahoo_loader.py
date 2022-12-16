import logging
from datetime import date
import pandas as pd
import yfinance as yf
from NNTrade.common import TimeFrame
from ..date_checks import check_date


def load_stock_candles(stock_code: str, from_dt: date, till_dt: date, timeframe: TimeFrame) -> pd.DataFrame:
    logger: logging.Logger = logging.getLogger("func yahoo_loader.load_stock_candles")
    logger.debug("Check input parameters")
    
    check_date(from_dt, till_dt)

    if timeframe.to_seconds() < 24*60*60:
        if (till_dt - from_dt).days > 30:
            raise AttributeError(
                f"For intraday stock quote allows only 30 days")


    logger.info("Start download from yahoo finance")
    from_date = from_dt.strftime('%Y-%m-%d')
    till_date = till_dt.strftime('%Y-%m-%d')

    logger.info(
        f"Download stock {stock_code} timeframe {timeframe.name}")
    ytf = timeframe_to_yfinance(timeframe)
    data: pd.DataFrame = yf.download(tickers=stock_code, start=from_date,
                                     end=till_date, interval=ytf)

    data.drop("Adj Close", inplace=True, axis=1)
    data.columns = [c.lower() for c in data.columns]
    data.index = data.index.rename('start_date_time')

    if len(data) == 0:
        raise AttributeError(
                f"No data for stock {stock_code}")

    return data

def timeframe_to_yfinance(tf: TimeFrame):
    # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    if tf == TimeFrame.MONTH:
        return "1mo"
    elif tf == TimeFrame.WEEK:
        return "1wk"
    elif tf == TimeFrame.DAY:
        return "1d"
    elif tf == TimeFrame.HOUR:
        return "1h"
    elif tf == TimeFrame.MINUTE30:
        return "30m"
    elif tf == TimeFrame.MINUTE15:
        return "15m"
    elif tf == TimeFrame.MINUTE5:
        return "5m"
