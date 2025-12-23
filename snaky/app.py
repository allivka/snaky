import json

from snaky import *

def run(config: Config) -> None:

    game: Game = Game(config)
    record: dict[str, int] = json.load(open(config["record_path"]))

    surface: pygame.Surface = pygame.display.set_mode(game.surface.get_size() + Vec2(config["stats_reserved_width"], 0))
    pygame.display.set_caption(config["caption"])
    pygame.display.set_icon(pygame.image.load(config["icon_path"]))

    font: pygame.font.Font = pygame.font.SysFont(config["font"], config["font_size"])

    info: stats.Stats = stats.Stats(font,
                                    text_color=pygame.Color((255, 213, 65)),
                                    padding=Vec2(0, 100),
                                    shift=Vec2(game.field.get_screen_size().x + config["stats_border_width"], config["stats_border_width"]),
                                    text_shift=Vec2(config["stats_text_shift"]),
                                    )

    clock: pygame.time.Clock = pygame.time.Clock()

    while not game.game_over:

        try:
            frame: pygame.Surface = game.play()
        except SnakyException as exception:
            print(exception)
            break
        else:
            surface.blit(frame, (0, 0))

        if game.score > record["record"]:
            record["record"] = game.score

        info.update(score=game.score, record=record["record"])
        pygame.draw.rect(surface, color=(89, 193, 53),
                         rect=pygame.Rect(info.shift.x - config["stats_border_width"],
                                          info.shift.y - config["stats_border_width"],
                                          config["stats_reserved_width"],
                                          surface.get_size()[1]))

        pygame.draw.rect(surface, color=(156, 219, 67),
                         rect=pygame.Rect(info.shift.x,
                                          info.shift.y,
                                          config["stats_reserved_width"] - config["stats_border_width"] * 2,
                                          surface.get_size()[1] - config["stats_border_width"] * 2))

        info.draw(surface)

        pygame.display.update()
        clock.tick(config["tick_rate"])

    json.dump(record, open(config["record_path"], "w"))
    pygame.quit()