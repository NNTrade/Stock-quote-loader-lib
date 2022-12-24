from __future__ import annotations
from .source import Source
from .chart_config import ChartConfig
from datetime import date
from typing import List, Dict
import json

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

  def to_dict(self)->Dict:
    return {"chart": self.chart.to_dict(), "date_from": self.date_from.strftime('%Y-%m-%d'), "date_till": self.date_till.strftime('%Y-%m-%d')}

  def __eq__(self, another: QuoteRequest):
    return hasattr(another, 'chart') and hasattr(another, "date_from") and hasattr(another, "date_till") and \
           self.chart == another.chart and self.date_from == another.date_from and self.date_till == another.date_till

  def __hash__(self):
    return hash(self.chart) ^ hash(self.date_from) ^ hash(self.date_till)

  def __str__(self) -> str:
   return json.dumps(self.to_dict(), sort_keys=True)