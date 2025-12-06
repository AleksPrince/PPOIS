import unittest
from pharma_company.planning.budget import Бюджет
from pharma_company.planning.sales_plan import ПланПродаж

class TestPlanning(unittest.TestCase):
    def test_budget_add_expense(self):
        b = Бюджет(1000.0)
        b.добавить_расход(200.0)
        self.assertEqual(b.остаток(), 800.0)

    def test_budget_add_income(self):
        b = Бюджет(1000.0)
        b.добавить_доход(500.0)
        self.assertEqual(b.остаток(), 1500.0)

    def test_sales_plan_add_drug(self):
        plan = ПланПродаж(1, "2025")
        plan.добавить_препарат("Анальгин")
        self.assertIn("Анальгин", plan.препараты)
