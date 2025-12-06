from dataclasses import dataclass
from typing import List
from pharma_company.exceptions import *

@dataclass
class СоглашениеОКонфиденциальности:
    """Соглашение о конфиденциальности с клиентом/партнёром."""
    id: int
    стороны: List[str]
    дата: str
    активно: bool = True

    def завершить(self):
        """Завершает действие соглашения."""
        self.активно = False

    def продлить(self, дата: str):
        """Продлевает соглашение."""
        self.дата = дата
