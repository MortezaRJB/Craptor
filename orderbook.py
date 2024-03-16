from decimal import Decimal
from typing import List, Dict
from datetime import datetime


class Order:

  def __init__(self, size: Decimal, is_Bid: bool) -> None:
    self.size             = size
    self.is_Bid           = is_Bid
    self.limit: Limit     = None
    self.timestamp        = datetime.now


class Limit:

  def __init__(self, price: Decimal) -> None:
    self.price                  = price
    self.orders: List[Order]    = None
    self.totalVolume            = Decimal('0')


class Orderbook:

  def __init__(self) -> None:
    self.asks: List['Limit']                  = []
    self.bids: List['Limit']                  = []
    self.askLimits: Dict[Decimal, 'Limit']    = {}
    self.bidLimits: Dict[Decimal, 'Limit']    = {}


