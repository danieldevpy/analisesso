from dataclasses import dataclass


@dataclass
class Element:
    name: str
    element_search: str
    type: None
    time: int = 10