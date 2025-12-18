import pygame
from typing import TypedDict
from pygame.math import Vector2 as Vec2
from math import radians, sin, cos

class Config(TypedDict):
    tick_rate: int
    icon_path: str

    map_chunk_path: str
    map_size_x: int
    map_size_y: int

    apple_path: str
    apple_centre_shift_x: float
    apple_centre_shift_y: float

    snake_head_path: str
    snake_tail_path: str
    snake_body_straight_path: str
    snake_body_blended_right_path: str

    snake_centre_shift_x: float
    snake_centre_shift_y: float

class Entity:

    def __init__(self, surface: pygame.Surface, chunk_size: Vec2, pos: Vec2 = (0, 0), centre_shift: tuple[float, float] = (0.0, 0.0)) -> None:
        self.surface = surface
        self.pos = pos
        self.chunk_size = chunk_size
        self.centre_shift = centre_shift

    def __str__(self) -> str:
        return f"pos={self.pos}, chunk_size={self.chunk_size}, centre_shift={self.centre_shift}\n\tsurface={self.surface}"

    def get_screen_pos(self, shift: Vec2 = (0, 0)) -> Vec2:
        return Vec2(self.pos[0] * self.chunk_size[0] + (self.chunk_size[0] // 2 - self.surface.get_size()[0] // 2) + int(self.chunk_size[0] * self.centre_shift[0]) + shift[0],
                self.pos[1] * self.chunk_size[1] + (self.chunk_size[1] // 2 - self.surface.get_size()[1] // 2) + int(self.chunk_size[1] * self.centre_shift[1]) + shift[1]
                )

    def draw(self, sf: pygame.Surface, shift: Vec2 = (0, 0)) -> None:
        sf.blit(self.surface, self.get_screen_pos(shift))