from NNTrade.common import TimeFrame

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