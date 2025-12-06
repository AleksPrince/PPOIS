from dataclasses import dataclass, field
from typing import List
from pharma_company.exceptions import *

@dataclass
class ОценкаРисков:
    """Оценка рисков по препарату и хранению."""
    id: int
    препарат: "Препарат"
    склад: Optional["Склад"] = None
    уровень: str = "средний"
    замечания: List[str] = field(default_factory=list)

    def добавить_замечание(self, текст: str):
        self.замечания.append(текст)

    def повысить_уровень(self):
        self.уровень = "высокий"


@dataclass
class СервисАналитики:
    """Сервис аналитики: анализ рисков и продаж."""
    id: int
    отчёты: List["ФинансовыйОтчёт"] = field(default_factory=list)
    риски: List[ОценкаРисков] = field(default_factory=list)
    активен: bool = True

    def добавить_отчёт(self, отчёт: "ФинансовыйОтчёт"):
        self.отчёты.append(отчёт)

    def добавить_оценку(self, оценка: ОценкаРисков):
        self.риски.append(оценка)


@dataclass
class СервисКомплаенса:
    """Сервис комплаенса: проверка регуляторных требований."""
    id: int
    стандарты: List["СтандартКачества"] = field(default_factory=list)
    лицензии_вендоров: dict[int, bool] = field(default_factory=dict)
    активен: bool = True

    def добавить_стандарт(self, стандарт: "СтандартКачества"):
        self.стандарты.append(стандарт)

    def проверить_лицензию(self, производитель: "Производитель") -> bool:
        производитель.проверить_лицензию()
        return True
