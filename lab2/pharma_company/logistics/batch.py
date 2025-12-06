from dataclasses import dataclass
from typing import Optional
from pharma_company.exceptions import *

@dataclass
class Партия:
    def __init__(self, id, товар, производитель=None, количество=0):
        self.id = id
        self.товар = товар
        self.производитель = производитель
        self.количество = количество

    def уменьшить(self, n):
        if n < 0 or n > self.количество:
            raise ValueError("Некорректное количество")
        self.количество -= n


@dataclass
class Упаковка:
    """Тип упаковки для партии препарата."""
    id: int
    тип: str
    единиц_в_коробке: int
    маркировка: Optional[str] = None

    def рассчитать_коробки(self, количество: int) -> int:
        return (количество + self.единиц_в_коробке - 1) // self.единиц_в_коробке

    def обновить_маркировку(self, текст: str):
        self.маркировка = текст


@dataclass
class СкладскаяЕдиница:
    """Складская единица хранения (SKU)."""
    id: int
    препарат: "Препарат"
    партия: Партия
    количество: int

    def списать(self, n: int):
        if n < 0 or n > self.количество:
            raise ОшибкаСкладскогоУчёта("Некорректное списание SKU.")
        self.количество -= n

    def пополнить(self, n: int):
        self.количество += n
