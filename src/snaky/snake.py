from .general import *
from enum import Enum

class BodyTileType(Enum):
    STRAIGHT = object()
    LEFT = object()
    RIGHT = object()

class BodyTile(Entity):
    def __init__(self, tile_type: BodyTileType, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.tile_type = tile_type

class Snake:
    def __init__(self, head: Entity, tail:Entity, body: list[Entity], direction: tuple[int, int]) -> None:
        self.head = head
        self.tail = tail
        self.body = body


