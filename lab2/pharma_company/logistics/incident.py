from dataclasses import dataclass
from typing import Optional
from pharma_company.exceptions import *

@dataclass
class ИнцидентКачества:
    """Инцидент качества по партии/препарату."""
    id: int
    препарат: "Препарат"
    партия: Optional["Партия"] = None
    описание: str = ""
    закрыт: bool = False

    def закрыть(self):
        self.закрыт = True

    def эскалировать(self):
        # Логика эскалации
        pass


@dataclass
class УведомлениеРегулятору:
    """Уведомление регулятору о событиях/нарушениях."""
    id: int
    препарат: Optional["Препарат"] = None
    описание: str = ""
    отправлено: bool = False

    def отправить(self):
        self.отправлено = True

    def отозвать(self):
        self.отправлено = False
