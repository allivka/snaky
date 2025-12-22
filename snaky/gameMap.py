
from .general import *

class MapMatrix:
    def __init__(self, size: Vec2) -> None:
        self.size = size
        self._matrix = [[False for _ in range(int(size[1]))] for _ in range(int(size[0]))]

    def is_valid_pos(self, pos: Vec2) -> bool:
        return 0 <= pos.x < self.size.x and 0 <= pos.y < self.size.y

    def validate_pos(self, pos: Vec2) -> bool:
        if not self.is_valid_pos(pos):
            raise IndexError("Position out of matrix bounds")

        return True

    def __getitem__(self, pos: Vec2) -> bool:
        self.validate_pos(pos)
        return self._matrix[int(pos.x)][int(pos.y)]

    def __setitem__(self, pos: Vec2, val: bool) -> None:
        self.validate_pos(pos)
        self._matrix[int(pos.x)][int(pos.y)] = val

    def fill(self, points: list[Vec2], value: bool = True) -> None:
        for point in points:
            self[point] = value

    def clear(self, value: bool = False) -> None:
        for i in range(int(self.size[0])):
            for j in range(int(self.size[1])):
                self._matrix[i][j] = value

    def set(self, points: list[tuple[Vec2, bool]]) -> None:
        for point in points:
            self[point[0]] = point[1]

    def sync(self, points: list[tuple[Vec2, bool]], fill_value: bool = False) -> None:
        self.clear(fill_value)
        self.set(points)

    def unfold(self) -> list[tuple[Vec2, bool]]:
        result = []

        for x in range(int(self.size[0])):
            result += [(Vec2(x, y), self._matrix[x][y]) for y in range(int(self.size[1]))]

        return result

class Map:

    def __init__(self, size: Vec2, chunk: pygame.Surface) -> None:

        self.matrix = MapMatrix(size)

        self.chunk_size : Vec2 = Vec2(chunk.get_size())
        screen_size = (self.chunk_size[0] * size[0], self.chunk_size[1] * size[1])
        self.surface = pygame.Surface(screen_size)

        for i in range(int(self.size[0])):
            for j in range(int(self.size[1])):
                self.surface.blit(chunk, (self.chunk_size[0] * i, self.chunk_size[1] * j))

    @property
    def size(self) -> Vec2:
        return self.matrix.size

    def __str__(self) -> str:
        return f"Game map:\n\nsize={self.size}\nchunk_size={self.chunk_size}\nsurface={self.surface}"

    def get_screen_size(self) -> Vec2:
        return Vec2(self.chunk_size[0] * self.size[0], self.chunk_size[1] * self.size[1])