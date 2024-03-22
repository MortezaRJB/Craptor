import unittest
from orderbook import Limit, Order, Orderbook
from decimal import Decimal

class TestLimit(unittest.TestCase):

  def test_limit(self):
    l = Limit(Decimal('10000'))
    buy_order1 = Order(True, Decimal('4'))
    buy_order2 = Order(True, Decimal('3'))
    buy_order3 = Order(True, Decimal('15'))

    l.add_order(buy_order1)
    l.add_order(buy_order2)
    l.add_order(buy_order3)
    l.delete_order(buy_order2)
    
    print(l)


class TestPlaceLimitOrder(unittest.TestCase):

  def test_place_limit_order(self):
    ob = Orderbook()
    sellOrder1 = Order(False, Decimal('5'))
    buyOrder = Order(True, Decimal('7'))
    sellOrder2 = Order(False, Decimal('6'))
    sellOrder3 = Order(False, Decimal('2'))
    ob.place_limit_order(Decimal('10000'), sellOrder1)
    ob.place_limit_order(Decimal('8500'), buyOrder)
    ob.place_limit_order(Decimal('7000'), sellOrder2)
    ob.place_limit_order(Decimal('7000'), sellOrder3)

    self.assertEqual(len(ob.bids), 1)
    self.assertEqual(len(ob.asks), 2)
    self.assertEqual(ob.askLimits[Decimal('7000')].totalVolume, Decimal('8'))


class TestPlaceMarketOrder(unittest.TestCase):

  def test_place_market_order_single_fill(self):
    ob = Orderbook()
    sell_limit_order = Order(False, Decimal('10'))
    ob.place_limit_order(Decimal('10000'), sell_limit_order)
    buy_market_order = Order(True, Decimal('4'))
    matches = ob.place_market_order(buy_market_order)

    self.assertEqual(len(ob.asks), 1)
    self.assertEqual(len(matches), 1)
    self.assertEqual(ob.ask_total_volume(), Decimal('6'))
    self.assertTrue(buy_market_order.is_filled)
    self.assertEqual(matches[0].bid, buy_market_order)
    self.assertEqual(matches[0].ask, sell_limit_order)
    self.assertEqual(matches[0].size_filled, Decimal('4'))
    self.assertEqual(matches[0].price, Decimal('10000'))
  
  def test_place_market_order_multi_fill(self):
    ob = Orderbook()
    buy_limit_order1 = Order(True, Decimal('4'))
    buy_limit_order2 = Order(True, Decimal('5'))
    buy_limit_order3 = Order(True, Decimal('15'))
    ob.place_limit_order(Decimal('9000'), buy_limit_order1)
    ob.place_limit_order(Decimal('7000'), buy_limit_order2)
    ob.place_limit_order(Decimal('10000'), buy_limit_order3)

    self.assertEqual(ob.bid_total_volume(), Decimal('24'))

    sell_market_order = Order(False, Decimal('20.9'))
    matches = ob.place_market_order(sell_market_order)

    self.assertEqual(len(matches), 3)
    # print(f'\n==> Matches: ', [str(mtch) for mtch in matches])


if __name__ == 'main':
  unittest.main()
