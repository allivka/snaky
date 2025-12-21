from .gameModule import *

pygame.init()

def run(config: Config) -> None:

    game: Game = Game(config)

    surface: pygame.Surface = pygame.display.set_mode(game.surface.get_size())
    pygame.display.set_caption(config["caption"])
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

