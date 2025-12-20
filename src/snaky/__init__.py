from pygame.examples.cursors import surf

from .gameModule import *
import json

def main(config_path: str = "config.json") -> None:
    config: Config = json.load(open(config_path))

    pygame.init()
    game: Game = Game(config)

    surface: pygame.Surface = pygame.display.set_mode(game.surface.get_size())
    pygame.display.set_caption("Snaky")
    pygame.display.set_icon(pygame.image.load(config["icon_path"]))

    clock: pygame.time.Clock = pygame.time.Clock()
    i = 1
    while True:
        surface.blit(game.play(), (0, 0))
        pygame.display.update()
        clock.tick(config["tick_rate"])




if __name__ == "__main__":
    main()

