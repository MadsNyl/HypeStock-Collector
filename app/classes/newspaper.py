from dataclasses import dataclass


@dataclass
class Newspaper():
    id: int
    provider: str
    name: str
    start_url: str
    base_url: str
