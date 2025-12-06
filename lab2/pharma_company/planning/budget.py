from dataclasses import dataclass, field
from typing import Dict, Optional
from pharma_company.exceptions import *

@dataclass
class Бюджет:
    def __init__(self, начальная_сумма: float = 0.0):
        """
        Класс для управления бюджетом компании.
        :param начальная_сумма: стартовый баланс бюджета
        """
        self.сумма = начальная_сумма
        self.расходы = []
        self.доходы = []

    def добавить_расход(self, value: float):
        """Добавить расход и уменьшить сумму бюджета"""
        if value < 0:
            raise ValueError("Расход не может быть отрицательным")
        self.расходы.append(value)
        self.сумма -= value
        return self.сумма

    def добавить_доход(self, value: float):
        """Добавить доход и увеличить сумму бюджета"""
        if value < 0:
            raise ValueError("Доход не может быть отрицательным")
        self.доходы.append(value)
        self.сумма += value
        return self.сумма

    def остаток(self) -> float:
        """Текущий баланс бюджета"""
        return self.сумма

    def использование(self) -> float:
        """Процент использования бюджета (расходы / (доходы+начальная сумма))"""
        total_income = sum(self.доходы) + (self.сумма + sum(self.расходы) - sum(self.доходы))
        if total_income == 0:
            return 0.0
        return (sum(self.расходы) / total_income) * 100


@dataclass
class СервисБюджета:
    """Сервис бюджета: операции с бюджетами препаратов."""
    id: int
    бюджеты: Dict[int, Бюджет] = field(default_factory=dict)
    ответственный: Optional["МенеджерПродаж"] = None
    активен: bool = True

    def зарегистрировать(self, препарат: "Препарат", бюджет: Бюджет):
        self.бюджеты[препарат.id] = бюджет

    def утвердить(self, препарат_id: int):
        b = self.бюджеты.get(препарат_id)
        if not b:
            raise ОшибкаОтчётности("Бюджет не найден.")
        b.утверждён = True
