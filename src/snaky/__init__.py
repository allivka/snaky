from .gameModule import *
import json

def main(config_path: str = "config.json") -> None:
    config: Config = json.load(open(config_path))

    pygame.init()
    game: Game = Game(config)

    surface: pygame.Surface = pygame.display.set_mode(game.surface.get_size())
    pygame.display.set_caption("Snaky")
    pygame.display.set_icon(pygame.image.load(config["icon_path"]))

    frame: pygame.Surface = pygame.display.get_surface()

    while True:

        try:
            frame = game.play()
        except SystemExit:
            break
        finally:
            surface.blit(frame, (0, 0))
            pygame.display.update()

    pygame.quit()
    exit(0)



if __name__ == "__main__":
    main()

