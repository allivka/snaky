from .general import *
from enum import Enum
from typing import Optional

class TileType(Enum):
    head = object()
    straight = object()
    left = object()
    right = object()
    tail = object()

type BodySprites = dict[TileType, pygame.Surface]

def angle_to_vec(angle: int) -> Vec2:
    rad = radians(angle)
    speed: Vec2 = Vec2(cos(rad), sin(rad))

class BodyTile:
    def __init__(self,

                 sprites: BodySprites,
                 chunk_size: Vec2,
                 pos: Vec2 = (0, 0),
                 centre_shift: tuple[float, float] = (0.0, 0.0),
                 tile_type: TileType = TileType.straight,
                 direction: int = 0
                 )-> None:

        self.entity = Entity(sprites[TileType.straight], chunk_size, pos, centre_shift)
        self.sprites = sprites
        self.tile_type = tile_type
        self.direction = direction

    def update(self, t: Optional[TileType] = None) -> None:
        if not t is None: self.tile_type = t
        self.entity.surface = self.sprites[self.tile_type]
        self.entity.surface = pygame.transform.rotate(self.entity.surface, self.direction + 90)

    def draw(self, sf: pygame.Surface, shift: Vec2 = (0, 0)) -> None:
        self.update()
        self.entity.draw(sf, shift)


type Body = list[BodyTile]


class Snake:
    def __init__(self,
                 sprites: BodySprites,
                 chunk_size: Vec2,
                 pos: Vec2 = (0, 0),
                 centre_shift: tuple[float, float] = (0.0, 0.0),
                 direction: int = 0,
                 body_length: int = 3
                 ) -> None:

        if body_length < 3: body_length = 3

        self.sprites = sprites
        self.body = [BodyTile(sprites, chunk_size, pos, centre_shift, TileType.tail, direction),
                     *[BodyTile(sprites, chunk_size, pos - angle_to_vec(direction) * (i + 1), centre_shift, TileType.tail, direction) for i in range(0, body_length - 2)],
                     BodyTile(sprites, chunk_size, pos - angle_to_vec(direction) * (body_length - 1), centre_shift, TileType.head, direction)
                     ]


    def update_view(self) -> None:
        for tile in self.body:
            tile.update()

    def draw(self, sf: pygame.Surface, shift: Vec2 = (0, 0)) -> None:
        for tile in self.body:
            tile.entity.draw(sf, shift)

    def forward(self, distance: int) -> None:
        speed: Vec2 = angle_to_vec(self.body[-1].direction) * distance

        self.body[-1].entity.pos += speed

        for i in range(len(self.body) - 2, -1, -1):
            pass




