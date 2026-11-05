from dataclasses import dataclass

@dataclass
class pokemon:
    id: int
    name: str
    types: list
    weight: int
    height: int
    sprites: dict
    stats: list
    moves: list
