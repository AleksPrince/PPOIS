from dataclasses import dataclass
from pharma_company.exceptions import *

@dataclass
class Рецепт:
    def __init__(self, id, пациент, препарат=None, врач="", срок_действия="", статус="активен"):
        self.id = id
        self.пaциент = пациент
        self.препарат = препарат
        self.врач = врач
        self.срок_действия = срок_действия
        self.статус = статус

    def закрыть(self):
        self.статус = "закрыт"
