import unittest
from pharma_company.planning.budget import Бюджет

class TestBudgetExtra(unittest.TestCase):
    def test_budget_income_and_expense(self):
        b = Бюджет(1000.0)
        b.добавить_доход(500.0)
        b.добавить_расход(200.0)
        self.assertEqual(b.остаток(), 1300.0)

    def test_budget_usage_percent(self):
        b = Бюджет(1000.0)
        b.добавить_расход(400.0)
        usage = b.использование()
        self.assertTrue(0 <= usage <= 100)
