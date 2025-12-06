import unittest
from pharma_company.services.quality import СервисКонтроляКачества
from pharma_company.services.misc import ЖурналСобытий

class TestServices(unittest.TestCase):
    def test_quality_add_standard(self):
        service = СервисКонтроляКачества(1)
        service.добавить_стандарт("ISO")
        self.assertIn("ISO", service.стандарты)

    def test_event_log_write(self):
        log = ЖурналСобытий()
        log.записать("Событие")
        self.assertEqual(len(log.события), 1)

    def test_event_log_clear(self):
        log = ЖурналСобытий()
        log.записать("Событие")
        log.очистить()
        self.assertEqual(len(log.события), 0)
