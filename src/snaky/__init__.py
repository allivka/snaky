import pygame
import json
from typing import TypedDict

class Config(TypedDict):
    tick_rate: int
    screen_width: int
    screen_height: int
    icon_path: str
    map_chunk_path: str
    map_size_x: int
    map_size_y: int

class Game:

    config : Config

    surface: pygame.Surface

    def __init__(self, config: Config):
        pygame.init()

        if not pygame.image.get_extended():
            raise "Current device doesn't support png image format!\n"

        self.config = config
        pygame.display.set_caption("Snaky")
        pygame.display.set_mode((config["screen_width"], config["screen_height"]))
        pygame.display.set_icon(pygame.image.load(config["icon_path"]))

        pygame.image.load(config["map_chunk_path"]).convert_alpha()

    def play(self) -> None:
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: exit()
                print(event)

            clock.tick(self.config["tick_rate"])


def main() -> None:
    c: Config = json.load(open("config.json"))
    game: Game = Game(c)

    game.play()


if __name__ == "__main__":
    main()