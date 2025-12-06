import unittest
from pharma_company.systems.crm import CRMСистема
from pharma_company.core.company import ФармацевтическаяКомпания
from pharma_company.core.drug import Препарат, Производитель

class TestSystems(unittest.TestCase):
    def test_crm_add_client(self):
        crm = CRMСистема(1)
        client = ФармацевтическаяКомпания(1, "ФармБел", True)
        crm.добавить_клиента(client)
        self.assertEqual(len(crm.клиенты), 1)

    def test_crm_add_contract(self):
        crm = CRMСистема(1)
        prod = Производитель(1, "БелМед", True, {})
        drug = Препарат(1, "Анальгин", prod, 10.0, False)
        contract = {"drug": drug}
        crm.добавить_контракт(contract)
        self.assertEqual(len(crm.контракты), 1)
