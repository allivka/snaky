from .general import *
from enum import Enum
from typing import Optional

class TileType(Enum):
    head = object()
    straight = object()
    left = object()
    right = object()
    tail = object()

    def __str__(self) -> str:
        return f"TileType:( name={self.name}, value={self.value})"

type BodySprites = dict[TileType, pygame.Surface]

class BodyTile:
    def __init__(
            self,
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

    def __str__(self) -> str:
        return f"tile_type={self.tile_type}, direction={self.direction}\n\tentity={self.entity}\n"

    def update(self, t: Optional[TileType] = None) -> None:
        if not t is None: self.tile_type = t
        self.entity.surface = self.sprites[self.tile_type]
        self.entity.surface = pygame.transform.rotate(self.entity.surface, -self.direction - 90)

    def draw(self, sf: pygame.Surface, shift: Vec2 = (0, 0)) -> None:
        self.update()
        self.entity.draw(sf, shift)


type Body = list[BodyTile]


class Snake:
    def __init__(
            self,
            sprites: BodySprites,
            chunk_size: Vec2,
            pos: Vec2 = (0, 0),
            centre_shift: tuple[float, float] = (0.0, 0.0),
            direction: int = 0,
            body_length: int = 3,
            speed: int = 1
            ) -> None:

        if body_length < 3:
            body_length = 3

        self.sprites = sprites
        self.chunk_size = chunk_size
        self.centre_shift = centre_shift

        self.body = [
            BodyTile(sprites, chunk_size, pos - angle_to_vec(direction) * (body_length - 1), centre_shift, TileType.tail, direction),
            *[BodyTile(sprites, chunk_size, pos - angle_to_vec(direction) * (i + 1), centre_shift, TileType.straight, direction) for i in range(0, body_length - 2)],
            BodyTile(sprites, chunk_size, pos, centre_shift, TileType.head, direction)
        ]

        self.direction = direction
        self.speed = speed

        self.update()

    @property
    def head(self) -> BodyTile:
        return self.body[-1]

    @property
    def tail(self) -> BodyTile:
        return self.body[0]

    def update(self) -> None:
        self.direction = fix_degrees(self.direction)
        for tile in self.body:
            tile.update()

    def draw(self, sf: pygame.Surface, shift: Vec2 = (0, 0)) -> None:
        for tile in self.body:
            tile.entity.draw(sf, shift)

    def forward(self, direction: int | None = None) -> None:

        if direction is None:
            direction = self.direction

        for _ in range(self.speed):

            for i in range(1, len(self.body) - 1):
                self.body[i].direction = fix_degrees(self.body[i + 1].direction)
                self.body[i].entity.pos = self.body[i + 1].entity.pos

            self.body[-1].direction = direction
            self.body[-1].entity.pos = self.body[-1].entity.pos + angle_to_vec(self.body[-1].direction)


        for i in range(1, len(self.body) - 1):

            if self.body[i].tile_type.value in (TileType.head, TileType.tail):
                continue

            diff: int = fix_degrees(fix_degrees(self.body[i + 1].direction) - fix_degrees(self.body[i].direction))

            if diff > 0:
                self.body[i].tile_type = TileType.right
            elif diff < 0:
                self.body[i].tile_type = TileType.left
            elif diff == 0:
                self.body[i].tile_type = TileType.straight

        self.body[0].direction = fix_degrees(self.body[1].direction)
        self.body[0].entity.pos = self.body[1].entity.pos - angle_to_vec(self.body[1].direction)

    def grow(self, length: int = 1) -> None:

        tail: BodyTile = self.tail
        self.tail.entity.pos -= angle_to_vec(self.tail.direction) * length

        self.body = (
            [self.tail] +
            [
                BodyTile(self.sprites,
                self.chunk_size,
                tail.entity.pos - angle_to_vec(tail.direction) * (i + 1),
                self.centre_shift, TileType.straight, tail.direction) for i in range(0, length)
            ] +
            self.body[1:]
        )

