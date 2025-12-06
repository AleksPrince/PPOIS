import unittest
from pharma_company.audit.audit_report import ОтчётАудита
from pharma_company.audit.training import ПланОбучения

class TestAudit(unittest.TestCase):
    def test_audit_add_note(self):
        report = ОтчётАудита(1)
        report.добавить_замечание("Ошибка хранения")
        self.assertEqual(len(report.замечания), 1)

    def test_training_add_listener(self):
        training = ПланОбучения(["Тема1"])
        training.добавить_слушателя("Иванов")
        self.assertEqual(len(training.слушатели), 1)
