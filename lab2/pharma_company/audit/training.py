from dataclasses import dataclass, field
from typing import List
from pharma_company.exceptions import *

@dataclass
class ПланОбучения:
    """План обучения сотрудников."""
    темы: List[str]
    слушатели: List["Сотрудник"] = field(default_factory=list)
    проведено: int = 0

    def добавить_слушателя(self, s: "Сотрудник"):
        """Добавляет слушателя на обучение."""
        self.слушатели.append(s)

    def провести(self):
        """Проводит занятие."""
        self.проведено += 1


@dataclass
class КейсПродаж:
    """Кейс продаж для аналитики."""
    id: int
    клиент: "Клиент"
    препарат: "Препарат"
    результат: str = "успех"

    def обновить_результат(self, текст: str):
        """Обновляет результат кейса."""
        self.результат = текст

    def кратко(self) -> str:
        """Возвращает краткое описание."""
        return f"{self.клиент.имя} — {self.препарат.название}: {self.результат}"
