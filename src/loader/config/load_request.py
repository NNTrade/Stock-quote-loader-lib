from .source import Source
from .quote_request import QuoteRequest

class LoadRequest:
  """Request for download quotes from source
  """
  def __init__(self, source: Source, quote_request:QuoteRequest):
    self.__source = source
    self.__quote_request = quote_request

  @property
  def source(self)->Source:
    return self.__source
  
  @property
  def quote_request(self)->QuoteRequest:
    return self.__quote_request
