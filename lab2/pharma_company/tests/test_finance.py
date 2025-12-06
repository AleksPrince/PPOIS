import unittest
from pharma_company.finance.cards import БанковскаяКарта
from pharma_company.finance.payments import АнтифродПравила, ПлатёжСервис
from pharma_company.exceptions import НедостаточноСредств, ТранзакцияОтклоненаАнтифродом

class TestFinance(unittest.TestCase):
    def test_card_balance(self):
        card = БанковскаяКарта("1111", 100.0)
        self.assertEqual(card.баланс, 100.0)

    def test_card_block_unblock(self):
        card = БанковскаяКарта("1111", 100.0)
        card.заблокировать()
        self.assertTrue(card.заблокирована)
        card.разблокировать()
        self.assertFalse(card.заблокирована)

    def test_payment_success(self):
        c1 = БанковскаяКарта("1111", 500.0)
        c2 = БанковскаяКарта("2222", 100.0)
        service = ПлатёжСервис(АнтифродПравила(лимит=1000))
        service.перевод(c1, c2, 200.0)
        self.assertEqual(c1.баланс, 300.0)
        self.assertEqual(c2.баланс, 300.0)

    def test_payment_insufficient(self):
        c1 = БанковскаяКарта("1111", 100.0)
        c2 = БанковскаяКарта("2222", 100.0)
        service = ПлатёжСервис(АнтифродПравила(лимит=1000))
        with self.assertRaises(НедостаточноСредств):
            service.перевод(c1, c2, 200.0)

    def test_payment_antifraud(self):
        c1 = БанковскаяКарта("1111", 2000.0)
        c2 = БанковскаяКарта("2222", 100.0)
        service = ПлатёжСервис(АнтифродПравила(лимит=500))
        with self.assertRaises(ТранзакцияОтклоненаАнтифродом):
            service.перевод(c1, c2, 600.0)
