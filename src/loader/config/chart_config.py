from __future__ import annotations
from NNTrade.common import TimeFrame
from typing import List

class ChartConfig:
  """Chart config include TimeFrame for download
  """
  def __init__(self, stock, timeframe: TimeFrame):
    self.__stock = stock
    self.__timeframe = timeframe

  @property
  def stock(self):
    return self.__stock
  
  @property
  def timeframe(self)->TimeFrame:
    return self.__timeframe

  @staticmethod
  def from_array(stock_list: List, timeframe_list: List[TimeFrame])->List[ChartConfig]:
    _ret:List[ChartConfig] = []
    for stock in stock_list:
      for tf in timeframe_list:
        _ret.append(ChartConfig(stock, tf))
    return _ret