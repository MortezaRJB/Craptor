from decimal import Decimal
from datetime import datetime


class Order:

  def __init__(self, size: Decimal, is_Bid: bool) -> None:
    self.size             = size
    self.is_Bid           = is_Bid
    self.limit            = None
    self.timestamp        = datetime.now

