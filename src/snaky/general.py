import pygame
from typing import TypedDict


class Config(TypedDict):
    tick_rate: int
    icon_path: str

    map_chunk_path: str
    map_size_x: int
    map_size_y: int

    apple_path: str
    apple_centre_shift_x: float
    apple_centre_shift_y: float

class Entity:

    def __init__(self, surface: pygame.Surface, pos: tuple[int, int], chunk_size: tuple[int, int], centre_shift: tuple[float, float]) -> None:
        self.surface = surface
        self.pos = pos
        self.chunk_size = chunk_size
        self.centre_shift = centre_shift

    def get_screen_pos(self, shift: tuple[int, int] = (0, 0)) -> tuple[int, int]:
        return (self.pos[0] * self.chunk_size[0] + (self.chunk_size[0] // 2 - self.surface.get_size()[0] // 2) + int(self.chunk_size[0] * self.centre_shift[0]) + shift[0],
                self.pos[1] * self.chunk_size[1] + (self.chunk_size[1] // 2 - self.surface.get_size()[1] // 2) + int(self.chunk_size[1] * self.centre_shift[1]) + shift[1]
                )

    def draw(self, sf: pygame.Surface, shift: tuple[int, int] = (0, 0)) -> None:
        sf.blit(self.surface, self.get_screen_pos(shift))