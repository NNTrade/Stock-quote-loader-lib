from __future__ import annotations
from enum import Enum

class Source(Enum):
  """list of avaliable Source

  Args:
      Enum (str): source name
  """
  Yahoo = "Yahoo"
  Moex = "Moex"