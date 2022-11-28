import logging
from datetime import date
from typing import Tuple
from NNTrade.common import TimeFrame
import pandas as pd
import investpy
from ..date_checks import check_date

def load_stock_candles(stock_code: str, country:str, from_dt: date, till_dt: date, timeframe: TimeFrame) -> pd.DataFrame:
    logger: logging.Logger = logging.getLogger("func inveting_com_loader.load_stock_candles")
    logger.debug("Check input parameters")
  
    check_date(from_dt, till_dt)

    logger.debug("Prepare input parameters")
    from_date, till_date = date_formating(from_dt, till_dt)
    interval = timeframe_to_investing_com(timeframe)

    investpy.get_stock_historical_data(stock=stock_code,
                                            country=country,
                                            from_date=from_date,
                                            to_date=till_date,
                                            interval=interval)

def date_formating(from_dt:date, till_dt:date)->Tuple[str,str]:
  from_date = from_dt.strftime('%d/%m/%Y')
  till_date = till_dt.strftime('%d/%m/%Y')
  return (from_date, till_date)

def timeframe_to_investing_com(tf: TimeFrame):
    # 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    if tf == TimeFrame.MONTH:
        return "Monthly"
    elif tf == TimeFrame.WEEK:
        return "Weekly"
    elif tf == TimeFrame.DAY:
        return "Daily"
    else:
        raise AttributeError(f"TimeFrame {tf.name} not supported for investing.com")