import unittest
from pharma_company.rules.dispensing import НастройкиОтпуска
from pharma_company.rules.antifraud import НастройкиАнтифрода

class TestRules(unittest.TestCase):
    def test_dispensing_update(self):
        settings = НастройкиОтпуска(True, 10, True)
        settings.обновить(False, 5)
        self.assertFalse(settings.требовать_рецепт)
        self.assertEqual(settings.ограничение_количества, 5)

    def test_antifraud_change(self):
        antifraud = НастройкиАнтифрода("rules", "high")
        antifraud.изменить("low")
        self.assertEqual(antifraud.чувствительность, "low")

    def test_antifraud_disable(self):
        antifraud = НастройкиАнтифрода("rules", "high")
        antifraud.выключить()
        self.assertFalse(antifraud.активны)
