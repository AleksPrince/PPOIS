from dataclasses import dataclass
from typing import List
from pharma_company.exceptions import *

@dataclass
class МаршрутПоставки:
    """Маршрут поставки от производителя к аптеке."""
    id: int
    производитель: "Производитель"
    аптека: "Аптека"
    план_точек: List[str]
    статус: str = "запланирован"

    def начать(self):
        self.статус = "в пути"

    def завершить(self):
        self.статус = "завершён"
