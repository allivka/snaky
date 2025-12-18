
from .general import *

class Map:

    def __init__(self, size: Vec2, chunk: pygame.Surface) -> None:

        self.size : Vec2 = size

        self.chunk_size : Vec2 = Vec2(chunk.get_size())
        screen_size = (self.chunk_size[0] * size[0], self.chunk_size[1] * size[1])
        self.surface = pygame.Surface(screen_size)

        for i in range(int(self.size[0])):
            for j in range(int(self.size[1])):
                self.surface.blit(chunk, (self.chunk_size[0] * i, self.chunk_size[1] * j))

    def __str__(self) -> str:
        return f"Game map:\n\nsize={self.size}\nchunk_size={self.chunk_size}\nsurface={self.surface}"

    def get_screen_size(self) -> Vec2:
        return Vec2(self.chunk_size[0] * self.size[0], self.chunk_size[1] * self.size[1])