from snaky import *

def run(config: Config) -> None:

    game: Game = Game(config)

    surface: pygame.Surface = pygame.display.set_mode(game.surface.get_size())
    pygame.display.set_caption(config["caption"])
    pygame.display.set_icon(pygame.image.load(config["icon_path"]))

    while not game.game_over:

        try:
            frame: pygame.Surface = game.play()
        except SnakyException as exception:
            print(exception)
            break
        else:
            surface.blit(frame, (0, 0))
            pygame.display.update()

    pygame.quit()