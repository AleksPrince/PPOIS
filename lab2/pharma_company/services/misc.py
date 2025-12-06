from dataclasses import dataclass, field
from typing import List, Optional
from pharma_company.exceptions import *

@dataclass
class ЖурналСобытий:
    """Журнал событий системы."""
    события: List[str] = field(default_factory=list)

    def записать(self, текст: str):
        self.события.append(текст)

    def очистить(self):
        self.события.clear()


@dataclass
class АвторизацияУстройства:
    """Авторизация устройства (POS/терминал)."""
    устройство_id: str
    владелец: "Аптека"
    активен: bool = True
    последняя_проверка: Optional[str] = None

    def деактивировать(self):
        self.активен = False

    def обновить_проверку(self, дата: str):
        self.последняя_проверка = дата


@dataclass
class СогласиеНаОбработкуДанных:
    """Согласие клиента на обработку данных."""
    клиент: "Клиент"
    дата: str
    отозвано: bool = False

    def отозвать(self):
        self.отозвано = True

    def активно(self) -> bool:
        return not self.отозвано
