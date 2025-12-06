from dataclasses import dataclass
from typing import Optional
from pharma_company.exceptions import *

@dataclass
class Оборудование:
    """Оборудование для работы с препаратами."""
    id: int
    название: str
    обслуживается: bool
    ответственный: Optional["Сотрудник"] = None
    состояние: str = "исправно"

    def провести_обслуживание(self):
        """Помечает оборудование как обслуженное."""
        self.обслуживается = True

    def вывести_из_эксплуатации(self):
        """Выводит оборудование из эксплуатации."""
        self.состояние = "выведено"
