from dataclasses import dataclass, field
from typing import List
from pharma_company.exceptions import *

@dataclass
class СервисЗаказаМатериалов:
    """Сервис заказа материалов у поставщиков."""
    id: int
    поставщики: List["Поставщик"] = field(default_factory=list)
    активен: bool = True
    заказы: List[str] = field(default_factory=list)

    def добавить_поставщика(self, поставщик: "Поставщик"):
        self.поставщики.append(поставщик)

    def оформить(self, описание: str):
        self.заказы.append(описание)


@dataclass
class ПланПоставок:
    """План поставок материалов и препаратов."""
    id: int
    поставщики: List["Поставщик"] = field(default_factory=list)
    препараты: List["Препарат"] = field(default_factory=list)
    точки: List[str] = field(default_factory=list)

    def добавить_поставщика(self, поставщик: "Поставщик"):
        self.поставщики.append(поставщик)

    def добавить_препарат(self, препарат: "Препарат"):
        self.препараты.append(препарат)
