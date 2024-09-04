from dataclasses import dataclass
from typing import List

@dataclass
class Filter:
    name: str
    values: List[str]

    def get_date(self):
        return [value.replace('/', '') for value in self.values]


@dataclass
class Relatorio:
    name: str
    columns: List[str]
    filters: List[Filter]
    surname: str = None

    def name_for_directory(self) -> str:
        if self.surname:
            return self.surname
        return self.name.replace(" ", "")
        