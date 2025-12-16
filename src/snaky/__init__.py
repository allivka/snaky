import pygame
import json
from typing import TypedDict

from pygame import Surface


class Config(TypedDict):
    tick_rate: int
    icon_path: str
    map_chunk_path: str
    map_size_x: int
    map_size_y: int

class Map:

    surface: pygame.Surface
    size: tuple[int, int]
    chuck_size: tuple[int, int]
    screen_size: tuple[int, int]

    def __init__(self, size: tuple[int, int], chunk: pygame.Surface):

        self.size = size

        self.chunk_size : tuple[int, int] = chunk.get_size()
        self.screen_size = (self.chunk_size[0] * size[0], self.chunk_size[1] * size[1])
        self.surface = pygame.Surface(self.screen_size)


        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.surface.blit(chunk, (self.chunk_size[0] * i, self.chunk_size[1] * j))


class Game:

    config : Config

    surface: pygame.Surface

    field: Map

    def __init__(self, config: Config):
        pygame.init()

        if not pygame.image.get_extended():
            raise "Current device doesn't support png image format!\n"

        self.config = config

        chunk : pygame.Surface = pygame.image.load(config["map_chunk_path"])
        self.field = Map((config["map_size_x"], config["map_size_y"]), chunk)

        self.surface = pygame.display.set_mode((self.field.size[0] * chunk.get_size()[0], self.field.size[1] * chunk.get_size()[1]))
        pygame.display.set_caption("Snaky")
        pygame.display.set_icon(pygame.image.load(config["icon_path"]))



    def play(self) -> None:
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: exit()

            self.surface.blit(self.field.surface, (0,0))

            pygame.display.update()
            clock.tick(self.config["tick_rate"])



def main(config_path: str) -> None:
    c: Config = json.load(open(config_path))
    game: Game = Game(c)

    game.play()
