import unittest
from pharma_company.logistics.batch import  Партия
from pharma_company.logistics.warehouse import  Склад
from pharma_company.core.drug import Препарат, Производитель

class TestLogistics(unittest.TestCase):
    def test_add_batch_to_storage(self):
        prod = Производитель(1, "БелМед", True, {})
        drug = Препарат(1, "Анальгин", prod, 10.0, False)
        batch = Партия(1, drug, None, 100)
        storage = Склад(1, "Минск", None, [])
        storage.добавить(batch)
        self.assertEqual(len(storage.партии), 1)

    def test_batch_reduce(self):
        prod = Производитель(1, "БелМед", True, {})
        drug = Препарат(1, "Анальгин", prod, 10.0, False)
        batch = Партия(1, drug, None, 100)
        batch.уменьшить(20)
        self.assertEqual(batch.количество, 80)
