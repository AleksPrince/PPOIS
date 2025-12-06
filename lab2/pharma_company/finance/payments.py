from dataclasses import dataclass
from pharma_company.exceptions import *
from pharma_company.finance.cards import БанковскаяКарта

@dataclass
class АнтифродПравила:
    лимит: float
    запрет_крупных: bool = True

    def проверка(self, сумма: float) -> bool:
        if self.запрет_крупных and сумма > self.лимит:
            return False
        return True

@dataclass
class ПлатёжСервис:
    антифрод: АнтифродПравила

    def перевод(self, источник: БанковскаяКарта, получатель: БанковскаяКарта, сумма: float):
        if источник.заблокирована or получатель.заблокирована:
            raise КартаЗаблокирована()
        if источник.баланс < сумма:
            raise НедостаточноСредств()
        if not self.антифрод.проверка(сумма):
            raise ТранзакцияОтклоненаАнтифродом()
        источник.баланс -= сумма
        получатель.баланс += сумма
        return True
