import unittest
from pharma_company.catalog.drug_catalog import СправочникПрепаратов, КатегорияПрепарата

class TestCatalog(unittest.TestCase):
    def test_add_drug_to_catalog(self):
        catalog = СправочникПрепаратов()
        drug = {"id": 1, "название": "Анальгин"}
        catalog.добавить(drug)
        self.assertIn(1, catalog.активные)

    def test_add_drug_to_category(self):
        cat = КатегорияПрепарата(1, "Анальгетики", "Болеутоляющие")
        cat.добавить("Анальгин")
        self.assertEqual(cat.размер(), 1)
