from dataclasses import dataclass, field
from typing import List, Optional
from pharma_company.exceptions import *

@dataclass
class ЭлектроннаяСистемаУчёта:
    """Система учёта препаратов и партий."""
    id: int
    аптека: "Аптека"
    протокол: Optional["ПротоколХранения"] = None
    версии: List[str] = field(default_factory=list)

    def обновить_версию(self, v: str):
        """Добавляет версию системы."""
        self.версии.append(v)

    def связать_протокол(self, протокол: "ПротоколХранения"):
        """Связывает протокол хранения."""
        self.протокол = протокол
