from dataclasses import dataclass, field
from typing import List
from pharma_company.exceptions import *
from pharma_company.exceptions import ЗапретРегулятора
@dataclass


class ФармацевтическаяКомпания:
    def __init__(self, id, название, лицензия_активна=True):
        self.id = id
        self.название = название
        self.лицензия_активна = лицензия_активна

    def проверить_лицензию(self):
        if not self.лицензия_активна:
            raise ЗапретРегулятора("Лицензия недействительна")
        return True
