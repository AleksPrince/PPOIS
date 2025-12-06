import unittest
from pharma_company.core.company import ФармацевтическаяКомпания
from pharma_company.core.drug import Препарат, Производитель, СертификатКачества, СтандартКачества

class TestCore(unittest.TestCase):
    def test_company_license(self):
        comp = ФармацевтическаяКомпания(1, "ФармБел", True)
        self.assertTrue(comp.проверить_лицензию())

    def test_drug_certificate(self):
        prod = Производитель(1, "БелМед", True, {})
        drug = Препарат(1, "Анальгин", prod, 10.0, False)
        cert = СертификатКачества(1, 1, "2025-01-01", "2026-01-01", True)
        drug.назначить_сертификат(cert)
        self.assertTrue(drug.проверить_сертификат())

    def test_quality_standard(self):
        std = СтандартКачества(1, "ISO", "Описание")
        self.assertEqual(std.название, "ISO")
