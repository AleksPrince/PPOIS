from dataclasses import dataclass, field
from typing import List
from pharma_company.exceptions import *

@dataclass
class HRСервис:
    """HR-сервис: работа с сотрудниками и назначениями."""
    id: int
    сотрудники: List["Сотрудник"] = field(default_factory=list)
    активен: bool = True
    политика: str = "стандарт"

    def нанять(self, сотрудник: "Сотрудник"):
        self.сотрудники.append(сотрудник)

    def уволить(self, сотрудник_id: int):
        self.сотрудники = [s for s in self.сотрудники if s.id != сотрудник_id]

