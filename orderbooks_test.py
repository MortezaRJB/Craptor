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


if __name__ == 'main':
  unittest.main()
