from .general import *

class Apple:
    surface: pygame.Surface
    pos: tuple[int, int]
    chunk_size: tuple[int, int]
    centre_shift: tuple[float, float]

    def __init__(self, surface: pygame.Surface, pos: tuple[int, int], chunk_size: tuple[int, int], centre_shift: tuple[float, float]) -> None:
        self.surface = surface
        self.pos = pos
        self.chunk_size = chunk_size
        self.centre_shift = centre_shift

    def get_screen_pos(self) -> tuple[int, int]:
        return (self.pos[0] * self.chunk_size[0] + (self.chunk_size[0] // 2 - self.surface.get_size()[0] // 2) + int(self.chunk_size[0] * self.centre_shift[0]),
                self.pos[1] * self.chunk_size[1] + (self.chunk_size[1] // 2 - self.surface.get_size()[1] // 2) + int(self.chunk_size[1] * self.centre_shift[1])
                )