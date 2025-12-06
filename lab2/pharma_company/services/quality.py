from dataclasses import dataclass, field
from typing import List
from pharma_company.exceptions import *

@dataclass
class СервисКонтроляКачества:
    def __init__(self):
        self.стандарты = []

    def добавить_стандарт(self, стандарт):
        self.стандарты.append(стандарт)

    def проверить(self, партия):
        return партия.количество > 0


@dataclass
class СервисИнспекцииХранения:
    """Сервис инспекции условий хранения."""
    id: int
    инспекции: List[str] = field(default_factory=list)
    активен: bool = True

    def зафиксировать(self, событие: str):
        self.инспекции.append(событие)

    def очистить(self):
        self.инспекции.clear()
