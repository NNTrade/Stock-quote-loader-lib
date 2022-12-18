from .source import Source
from .chart_config import ChartConfig
from datetime import date


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
