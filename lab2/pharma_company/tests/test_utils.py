import unittest
from pharma_company.utils.loyalty import КартаЛояльности

class TestUtils(unittest.TestCase):
    def test_loyalty_points(self):
        card = КартаЛояльности(1, None, 0)
        card.начислить(250.0)
        self.assertEqual(card.баллы, 25)

    def test_loyalty_spend(self):
        card = КартаЛояльности(1, None, 30)
        card.списать(10)
        self.assertEqual(card.баллы, 20)
