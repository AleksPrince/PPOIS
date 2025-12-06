from dataclasses import dataclass, field
from typing import Optional, Dict, List
from pharma_company.exceptions import *

@dataclass
class Производитель:
    def __init__(self, id, название, лицензия_активна=True, контакты=None):
        self.id = id
        self.название = название
        self.лицензия_активна = лицензия_активна
        self.контакты = контакты or {}

class СертификатКачества:
    def __init__(self, id, препарат_id, дата_выдачи, срок_действия, выдан=True):
        self.id = id
        self.препарат_id = препарат_id
        self.дата_выдачи = дата_выдачи
        self.срок_действия = срок_действия
        self.выдан = выдан

class СтандартКачества:
    def __init__(self, id, название, описание, минимальные_требования=""):
        self.id = id
        self.название = название
        self.описание = описание
        self.минимальные_требования = минимальные_требования

class Препарат:
    def __init__(self, id, название, производитель, цена, требование_рецепта=False):
        self.id = id
        self.название = название
        self.производитель = производитель
        self.цена = цена
        self.требование_рецепта = требование_рецепта
        self._сертификат = None

    def назначить_сертификат(self, сертификат: СертификатКачества):
        self._сертификат = сертификат

    def проверить_сертификат(self):
        return self._сертификат is not None and self._сертификат.выдан
