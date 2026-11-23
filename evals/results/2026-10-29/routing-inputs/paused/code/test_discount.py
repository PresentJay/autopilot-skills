import unittest
from discount import discount
class DiscountTests(unittest.TestCase):
    def test_cap(self):
        self.assertEqual(discount(100, 150), 0)
    def test_standard(self):
        self.assertEqual(discount(100, 25), 75)
