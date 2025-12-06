from dataclasses import dataclass, field
from typing import Dict
from pharma_company.exceptions import *

@dataclass
class КаталогПрепаратов:
    def __init__(self):
        self.активные = {}

    def добавить(self, препарат):
        # тесты ожидают, что у препарата есть .id
        if isinstance(препарат, dict):
            # если вдруг словарь — берём ключ 'id'
            self.активные[препарат["id"]] = препарат
        else:
            self.активные[препарат.id] = препарат



@dataclass
class КатегорияПрепарата:
    """Категория препарата."""
    id: int
    название: str
    описание: str
    препараты: list["Препарат"] = field(default_factory=list)

    def добавить(self, препарат: "Препарат"):
        """Добавляет препарат в категорию."""
        self.препараты.append(препарат)

    def размер(self) -> int:
        """Возвращает число препаратов в категории."""
        return len(self.препараты)
