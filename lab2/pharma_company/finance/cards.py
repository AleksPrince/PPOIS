from dataclasses import dataclass
from pharma_company.exceptions import *

from typing import Optional

@dataclass
class БанковскаяКарта:
    номер: str
    баланс: float
    заблокирована: bool = False
    владелец: Optional["УчётнаяЗапись"] = None  # ← добавляем

    def заблокировать(self): self.заблокирована = True
    def разблокировать(self): self.заблокирована = False
