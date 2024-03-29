from decimal import Decimal
from typing import List, Dict
from datetime import datetime
from functools import total_ordering


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


@total_ordering
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
        removed_order = o
        break
    if removed_order:
      removed_order.limit = None
      self.orders.pop(index)
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
    orders_to_delete = []

    for o in self.orders:
      if order.is_filled: break
      matched = self.fill_order(o, order)
      if matched:
        matches.append(matched)
        self.totalVolume -= matched.size_filled
        if o.is_filled: orders_to_delete.append(o)
    
    for o in orders_to_delete:
      self.delete_order(o)
    
    return matches
  
  def __str__(self) -> str:
    return f"Limit: price[{self.price}], orders#[{len(self.orders)}], volume[{self.totalVolume}]"
  
  def __le__(self, obj):
    return self.price < obj.price
  
  def __eq__(self, obj) -> bool:
    return self.price == obj.price


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
  
  def sorted_asks(self) -> List['Limit']:
    return sorted(self.asks, reverse=False)
  
  def sorted_bids(self) -> List['Limit']:
    return sorted(self.bids, reverse=True)
  
  def clear_limit(self, is_bid_limit: bool, limit: Limit):
    if is_bid_limit:
      self.bidLimits.pop(limit.price)
      self.bids.remove(limit)
    else:
      self.askLimits.pop(limit.price)
      self.asks.remove(limit)

  def place_market_order(self, order: Order):
    matches = []
    if order.is_Bid:
      if order.size > self.ask_total_volume():
        raise ValueError(f'Bid-Order Size Out of Range! total[{self.ask_total_volume}],  order-size[{order.size}]')
      else:
        for lim in self.sorted_asks():
          there_were_matches = lim.fill(order)
          if there_were_matches:
            matches.extend(there_were_matches)
            if len(lim.orders) == 0: self.clear_limit(False, lim)

    else: #>> order.is_Ask
      if order.size > self.bid_total_volume():
        raise ValueError(f'Ask-Order Size Out of Range! total[{self.bid_total_volume}],  order-size[{order.size}]')
      else:
        for lim in self.sorted_bids():
          there_were_matches = lim.fill(order)
          if there_were_matches:
            matches.extend(there_were_matches)
            if len(lim.orders) == 0: self.clear_limit(True, lim)
    
    return matches
  
  def cancel_order(self, order: Order):
    limit = order.limit
    limit.delete_order(order)

