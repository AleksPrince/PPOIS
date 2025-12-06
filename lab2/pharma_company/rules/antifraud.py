from dataclasses import dataclass, field
from typing import List
from pharma_company.exceptions import *

@dataclass
class НастройкиАнтифрода:
    """Настройки антифрода для платёжного сервиса."""
    правила: "АнтифродПравила"
    чувствительность: str
    активны: bool = True

    def изменить(self, чувствительность: str):
        """Меняет чувствительность антифрода."""
        self.чувствительность = чувствительность

    def выключить(self):
        """Выключает антифрод."""
        self.активны = False


@dataclass
class РегистраторОпераций:
    """Регистратор операций для антифрода и аудита."""
    операции: List[str] = field(default_factory=list)
    лимит: int = 1000

    def записать(self, операция: str):
        """Записывает операцию."""
        if len(self.операции) >= self.лимит:
            self.операции.pop(0)
        self.операции.append(операция)

    def очистить(self):
        """Очищает журнал операций."""
        self.операции.clear()
