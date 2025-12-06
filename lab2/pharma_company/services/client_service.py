from dataclasses import dataclass, field
from typing import List
from pharma_company.exceptions import *

@dataclass
class СервисРаботыСКлиентами:
    """Сервис по работе с клиентами и контрактами."""
    id: int
    клиенты: List["Клиент"] = field(default_factory=list)
    контракты: List["Контракт"] = field(default_factory=list)
    активен: bool = True

    def зарегистрировать(self, клиент: "Клиент"):
        self.клиенты.append(клиент)

    def оформить_контракт(self, контракт: "Контракт"):
        self.контракты.append(контракт)
