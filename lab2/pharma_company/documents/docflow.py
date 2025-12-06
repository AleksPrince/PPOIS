from dataclasses import dataclass, field
from typing import List
from pharma_company.exceptions import *

@dataclass
class СервисДокументооборота:
    """Сервис документооборота: работа с рецептами и контрактами."""
    id: int
    рецепты: List["Рецепт"] = field(default_factory=list)
    контракты: List["Контракт"] = field(default_factory=list)
    активен: bool = True

    def зарегистрировать_рецепт(self, рецепт: "Рецепт"):
        """Регистрирует рецепт."""
        self.рецепты.append(рецепт)

    def зарегистрировать_контракт(self, контракт: "Контракт"):
        """Регистрирует контракт."""
        self.контракты.append(контракт)

