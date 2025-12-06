from dataclasses import dataclass, field
from typing import List, Optional
from pharma_company.exceptions import *

@dataclass
class ОтчётАудита:
    """Отчёт аудита по складам/системам."""
    id: int
    склад: Optional["Склад"] = None
    система: Optional["ЭлектроннаяСистемаУчёта"] = None
    замечания: List[str] = field(default_factory=list)

    def добавить_замечание(self, текст: str):
        """Добавляет замечание в отчёт."""
        self.замечания.append(текст)

    def итог(self) -> str:
        """Возвращает краткий итог."""
        return f"Замечаний: {len(self.замечания)}"
