from dataclasses import dataclass, field
from typing import List
from pharma_company.exceptions import *

@dataclass
class ФинансовыйОтчёт:
    """Финансовый отчёт по препарату."""
    id: int
    препарат: "Препарат"
    доход: float
    расход: float
    баланс: float
    период: str

    def пересчитать(self):
        self.баланс = self.доход - self.расход

    def проверить_валидность(self) -> bool:
        if self.баланс is None:
            raise ОшибкаОтчётности("Баланс не рассчитан.")
        return True


@dataclass
class СервисОтчётности:
    """Сервис отчётности: формирование отчетов."""
    id: int
    отчёты: List[ФинансовыйОтчёт] = field(default_factory=list)
    активен: bool = True
    формат: str = "xlsx"

    def добавить(self, отчёт: ФинансовыйОтчёт):
        self.отчёты.append(отчёт)

    def выгрузить(self) -> int:
        return len(self.отчёты)
