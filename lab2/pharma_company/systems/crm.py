from dataclasses import dataclass, field
from typing import List
from pharma_company.exceptions import *

@dataclass
class CRMСистема:
    """CRM: управление клиентами и контрактами."""
    id: int
    клиенты: List["Клиент"] = field(default_factory=list)
    контракты: List["Контракт"] = field(default_factory=list)
    активна: bool = True

    def добавить_клиента(self, клиент: "Клиент"):
        self.клиенты.append(клиент)

    def добавить_контракт(self, контракт: "Контракт"):
        self.контракты.append(контракт)
