import pygame
from typing import TypedDict
from pygame.math import Vector2 as Vec2
from math import radians, sin, cos

class SnakyException(Exception):
    """Base exception for all snaky exceptions"""

def angle_to_vec(angle: int) -> Vec2:
    rad = radians(angle)
    return Vec2(cos(rad), sin(rad))

def fix_degrees(angle: int) -> int:
    t: int = (angle + 180) % 360 - 180
    return t if t != -180 else 180

class Config(TypedDict):

    record_path: str

    stats_reserved_width: int
    stats_border_width: int
    stats_text_shift: tuple[int, int]

    font: str
    font_size: int

    tick_rate: int
    icon_path: str
    caption: str

    map_chunk_path: str
    map_size_x: int
    map_size_y: int

    apple_path: str
    apple_centre_shift_x: float
    apple_centre_shift_y: float
    apple_start_pos: tuple[int, int]

    snake_head_path: str
    snake_tail_path: str
    snake_body_straight_path: str
    snake_body_blended_right_path: str

    snake_centre_shift_x: float
    snake_centre_shift_y: float

    control_time_gap: int
    move_update_gap: int
    min_move_update_gap: int
    gap_per_score: int

    start_length: int
    start_direction: int
    start_pos: tuple[int, int]


class ResourceBank:
    def __init__(self, config: Config):
        self.map_chunk: pygame.Surface = pygame.image.load(config["map_chunk_path"])

        self.apple: pygame.Surface = pygame.image.load(config["apple_path"])

        self.snake_head: pygame.Surface = pygame.image.load(config["snake_head_path"])
        self.snake_tail: pygame.Surface = pygame.image.load(config["snake_tail_path"])
        self.snake_body_straight: pygame.Surface = pygame.image.load(config["snake_body_straight_path"])
        self.snake_body_blended_right: pygame.Surface = pygame.image.load(config["snake_body_blended_right_path"])
        self.snake_body_blended_left: pygame.Surface = pygame.transform.flip(self.snake_body_blended_right, True, False)

class Entity:

    def __init__(self, surface: pygame.Surface, chunk_size: Vec2, pos: Vec2 = (0, 0), centre_shift: tuple[float, float] = (0.0, 0.0)) -> None:
        self.surface = surface
        self.pos = pos
        self.chunk_size = chunk_size
        self.centre_shift = centre_shift

    def __str__(self) -> str:
        return f"pos={self.pos}, chunk_size={self.chunk_size}, centre_shift={self.centre_shift}\n"

    def get_screen_pos(self, shift: Vec2 = (0, 0)) -> Vec2:
        return Vec2(self.pos[0] * self.chunk_size[0] + (self.chunk_size[0] // 2 - self.surface.get_size()[0] // 2) + int(self.chunk_size[0] * self.centre_shift[0]) + shift[0],
                self.pos[1] * self.chunk_size[1] + (self.chunk_size[1] // 2 - self.surface.get_size()[1] // 2) + int(self.chunk_size[1] * self.centre_shift[1]) + shift[1]
                )

    def draw(self, sf: pygame.Surface, shift: Vec2 = (0, 0)) -> None:
        sf.blit(self.surface, self.get_screen_pos(shift))