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


if __name__ == 'main':
  unittest.main()
