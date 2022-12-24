from __future__ import annotations
import json
from .source import Source
from .quote_request import QuoteRequest
from typing import Dict

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

  def to_dict(self)->Dict:
    return {"source": self.source.value, "quote_request": self.quote_request.to_dict()}

  def __eq__(self, another: LoadRequest):
    return hasattr(another, 'source') and hasattr(another, "quote_request") and \
           self.source == another.source and self.quote_request == another.quote_request

  def __hash__(self):
    return hash(self.source) ^ hash(self.quote_request)

  def __str__(self) -> str:
   return json.dumps(self.to_dict(), sort_keys=True)