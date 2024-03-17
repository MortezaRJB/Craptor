from decimal import Decimal
from typing import List, Dict
from datetime import datetime


class Order:

  def __init__(self, is_Bid: bool, size: Decimal) -> None:
    self.size             = size
    self.is_Bid           = is_Bid
    self.limit: Limit     = None
    self.timestamp        = datetime.now


class Limit:

  def __init__(self, price: Decimal) -> None:
    self.price                  = price
    self.orders: List[Order]    = []
    self.totalVolume            = Decimal('0')
  
  def add_order(self, order: Order):
    order.limit = self
    self.orders.append(order)
    self.totalVolume += order.size
  
  def delete_order(self, order: Order):
    removed_order = None
    for index, o in enumerate(self.orders):
      if o == order:
        removed_order = self.orders.pop(index)
        break
    if removed_order:
      removed_order.limit = None
      self.totalVolume -= removed_order.size
  
  def __str__(self) -> str:
    return f"Limit: price[{self.price}], orders#[{len(self.orders)}], volume[{self.totalVolume}]"


class Orderbook:

  def __init__(self) -> None:
    self.asks: List['Limit']                  = []
    self.bids: List['Limit']                  = []
    self.askLimits: Dict[Decimal, 'Limit']    = {}
    self.bidLimits: Dict[Decimal, 'Limit']    = {}
  
  def place_limit_order(self, price: Decimal, order: Order):
    if order.is_Bid:
      limit = self.bidLimits.get(price, None)
    else:
      limit = self.askLimits.get(price, None)
    
    if not limit:
      limit = Limit(price)
      if order.is_Bid:
        self.bids.append(limit)
        self.bidLimits[price] = limit
      else:
        self.asks.append(limit)
        self.askLimits[price] = limit
    
    limit.add_order(order)

