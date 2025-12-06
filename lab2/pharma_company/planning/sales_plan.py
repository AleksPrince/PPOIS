from dataclasses import dataclass, field
from typing import Dict, List
from pharma_company.exceptions import *

@dataclass
class ПланПродаж:
    def __init__(self, id, год, цели_по_месяцам=None, ответственный=""):
        self.id = id
        self.год = год
        self.цели_по_месяцам = цели_по_месяцам or {}
        self.ответственный = ответственный

    def добавить_препарат(self, название, объём=0):
        self.цели_по_месяцам[название] = объём


@dataclass
class Задача:
    """Задача в графике продаж."""
    id: int
    название: str
    период: str
    исполнители: List["Сотрудник"] = field(default_factory=list)
    статус: str = "новая"
    связанный_препарат: Optional["Препарат"] = None

    def назначить(self, сотрудник: "Сотрудник"):
        self.исполнители.append(сотрудник)

    def завершить(self):
        self.статус = "завершена"


@dataclass
class Веха:
    """Веха плана продаж."""
    id: int
    название: str
    дата: str
    достигнута: bool = False
    связанная_задача: Optional[Задача] = None

    def установить_достигнута(self):
        self.достигнута = True

    def связать_задачу(self, задача: Задача):
        self.связанная_задача = задача


@dataclass
class ГрафикПродаж:
    """График продаж с задачами и вехами."""
    id: int
    план: ПланПродаж
    задачи: List[Задача] = field(default_factory=list)
    вехи: List[Веха] = field(default_factory=list)
    утверждён: bool = False

    def добавить_задачу(self, задача: Задача):
        self.задачи.append(задача)

    def есть_конфликт(self) -> bool:
        seen = set()
        for z in self.задачи:
            for s in z.исполнители:
                key = (s.id, z.период)
                if key in seen:
                    return True
                seen.add(key)
        return False
