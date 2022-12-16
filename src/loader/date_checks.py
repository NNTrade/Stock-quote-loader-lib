from datetime import date
import logging

def check_date(from_dt:date, till_dt:date):
  logger: logging.Logger = logging.getLogger("func check_date")
  logger.debug("Check dates")
  if till_dt <= from_dt:
      raise AttributeError(
              f"From date ({from_dt.strftime('%Y-%m-%d')}) should be less than Till date ({till_dt.strftime('%Y-%m-%d')})")
