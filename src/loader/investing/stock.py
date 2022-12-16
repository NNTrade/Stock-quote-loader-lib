class InvestingStock:
  def __init__(self, stock: str, country:str) -> None:
    self.Stock = stock
    self.Country = country
    pass

  def __str__(self) -> str:
    return f"{self.Country} {self.Stock}"