from dataclasses import dataclass, field
from typing import List, Tuple
from pharma_company.exceptions import *

@dataclass
class ПротоколХранения:
    """Протокол хранения: условия и актуальность."""
    id: int
    версия: str
    актуален: bool
    температура_диапазон: Tuple[float, float]
    влажность_макс: float

    def проверить(self, температура: float, влажность: float) -> bool:
        tmin, tmax = self.температура_диапазон
        if not (tmin <= температура <= tmax) or влажность > self.влажность_макс:
            raise НарушениеТемпературногоРежима("Нарушение условий хранения.")
        return True

    def обновить_версию(self, версия: str):
        self.версия = версия


@dataclass
class Склад:
    def __init__(self, название):
        self.название = название
        self._товары = []

    def добавить(self, партия):
        self._товары.append(партия)

    def итого(self):
        return sum(p.количество for p in self._товары)
