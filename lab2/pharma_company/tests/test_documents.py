import unittest
from pharma_company.documents.recipe import Рецепт
from pharma_company.core.drug import Препарат, Производитель

class TestDocuments(unittest.TestCase):
    def test_recipe_add_drug(self):
        prod = Производитель(1, "БелМед", True, {})
        drug = Препарат(1, "Анальгин", prod, 10.0, False)
        recipe = Рецепт(1, "Иванов")
        recipe.добавить_препарат(drug)
        self.assertEqual(len(recipe.препараты), 1)

    def test_recipe_close(self):
        recipe = Рецепт(1, "Иванов")
        recipe.закрыть()
        self.assertEqual(recipe.статус, "закрыт")
