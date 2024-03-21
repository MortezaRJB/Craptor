from decimal import Decimal
from typing import List, Dict
from datetime import datetime


class Order:

  def __init__(self, is_Bid: bool, size: Decimal) -> None:
    self.size             = size
    self.is_Bid           = is_Bid
    self.limit: Limit     = None
    self.timestamp        = datetime.now
  
  @property
  def is_filled(self):
    return self.size == 0


class Match:
  def __init__(self, bid: Order, ask: Order, size_filled: Decimal, price: Decimal) -> None:
    self.bid            = bid
    self.ask            = ask
    self.size_filled    = size_filled
    self.price          = price
  
  def __str__(self) -> str:
    return '{'+f"bid[{self.bid.size}], ask[{self.ask.size}], sizefilled[{self.size_filled}], price[{self.price}]"+'}'


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
  
  def fill_order(self, existing_order: Order, new_order: Order):
    size_filled = Decimal('0')
    if existing_order.is_Bid:
      bid = existing_order
      ask = new_order
    else:
      bid = new_order
      ask = existing_order
    if existing_order.size >= new_order.size:
      existing_order.size -= new_order.size
      size_filled = new_order.size
      new_order.size = Decimal('0')
    else:
      new_order.size -= existing_order.size
      size_filled = existing_order.size
      existing_order.size = Decimal('0')

    return Match(bid, ask, size_filled, self.price)
  
  def fill(self, order: Order):
    matches = []
    for o in self.orders:
      if order.is_filled:
        break
      matched = self.fill_order(o, order)
      if matched:
        matches.append(matched)
        self.totalVolume -= matched.size_filled
    return matches
  
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

  def bid_total_volume(self):
    total_vol = Decimal('0')
    for lim in self.bids:
      total_vol += lim.totalVolume
    return total_vol

  def ask_total_volume(self):
    total_vol = Decimal('0')
    for lim in self.asks:
      total_vol += lim.totalVolume
    return total_vol

  def place_market_order(self, order: Order):
    matches = []
    if order.is_Bid:
      if order.size > self.ask_total_volume():
        raise ValueError(f'Bid-Order Size Out of Range! total[{self.ask_total_volume}],  order-size[{order.size}]')
      else:
        for lim in self.asks:
          limit_matches = lim.fill(order)
          if limit_matches:
            matches.extend(limit_matches)
    else: #>> o.is_Ask
      if order.size > self.bid_total_volume():
        raise ValueError(f'Ask-Order Size Out of Range! total[{self.bid_total_volume}],  order-size[{order.size}]')
      else:
        for lim in self.bids:
          limit_matches = lim.fill(order)
          if limit_matches:
            matches.extend(limit_matches)
    return matches

