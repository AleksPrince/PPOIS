from dataclasses import dataclass, field
from typing import List, Optional
from pharma_company.exceptions import *

@dataclass
class ЖурналСобытий:
    """Журнал событий системы."""
    события: List[str] = field(default_factory=list)

    def записать(self, текст: str):
        """Записывает событие."""
        self.события.append(текст)

    def очистить(self):
        """Очищает журнал."""
        self.события.clear()


@dataclass
class Квитанция:
    """Квитанция об оплате."""
    id: int
    заказ: "Заказ"
    сумма: float
    дата: str
    валидна: bool = True

    def аннулировать(self):
        """Аннулирует квитанцию."""
        self.валидна = False

    def подтвердить(self):
        """Подтверждает квитанцию."""
        self.валидна = True


@dataclass
class РегистраторОпераций:
    """Регистратор операций для антифрода и аудита."""
    операции: List[str] = field(default_factory=list)
    лимит: int = 1000

    def записать(self, операция: str):
        """Записывает операцию."""
        if len(self.операции) >= self.лимит:
            self.операции.pop(0)
        self.операции.append(операция)

    def очистить(self):
        """Очищает журнал операций."""
        self.операции.clear()
