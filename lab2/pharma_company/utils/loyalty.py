from dataclasses import dataclass
from pharma_company.exceptions import *

@dataclass
class КартаЛояльности:
    def __init__(self, id, владелец, бонусы=0):
        self.id = id
        self.владелец = владелец
        self.бонусы = бонусы

    def начислить(self, сумма):
        self.бонусы += сумма

    def списать(self, сумма):
        if сумма > self.бонусы:
            raise ValueError("Недостаточно бонусов")
        self.бонусы -= сумма
