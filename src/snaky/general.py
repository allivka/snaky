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
