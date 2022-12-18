from __future__ import annotations
from .source import Source
from .chart_config import ChartConfig
from datetime import date
from typing import List

class QuoteRequest:
  """Request for download quote candle from source
  
  """
  def __init__(self, chart: ChartConfig, date_from:date, date_till:date):
    self.__chart = chart
    self.__date_from = date_from
    self.__date_till = date_till

  @property
  def chart(self)->ChartConfig:
    return self.__chart

  @property
  def date_from(self)->date:
    return self.__date_from
  
  @property
  def date_till(self)->date:
    return self.__date_till

  @staticmethod
  def from_array(chart_list:List[ChartConfig], date_from:date, date_till:date) -> List[QuoteRequest]:
    return [QuoteRequest(chart, date_from, date_till) for chart in chart_list]