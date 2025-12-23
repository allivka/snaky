import json
from snaky import *

def run(config: Config) -> None:

    game: Game = Game(config)

    with open(config["records_path"]) as r:
        records: dict = json.load(r)

    surface: pygame.Surface = pygame.display.set_mode(game.surface.get_size() + Vec2(config["stats_reserved_width"], 0))
    pygame.display.set_caption(config["caption"])
    pygame.display.set_icon(pygame.image.load(config["icon_path"]))

    font: pygame.font.Font = pygame.font.SysFont(config["font"], config["font_size"])

    current_record_name: str = "x".join((str(int(game.field.size.x)), str(int(game.field.size.y))))

    if records.get(current_record_name) is None:
        records[current_record_name] = game.score

    info: stats.Stats = stats.Stats(
        font,
        text_color=pygame.Color((255, 213, 65)),
        padding=Vec2(0, 100),
        shift=Vec2(game.field.get_screen_size().x + config["stats_border_width"], config["stats_border_width"]),
        text_shift=Vec2(config["stats_text_shift"]),
        current_record_name=current_record_name,
        other_records=records
        )

    f: pygame.font.Font = pygame.font.SysFont(config["font"], config["font_size"]  * 5)
    f.set_bold(True)
    f.set_italic(True)

    menu: menuModule.Menu = menuModule.Menu(
        size=Vec2(surface.get_size()),
        shift=Vec2(),
        text_color=info.text_color,
        font_size=config["font_size"]  * 5,
        font_name=config["font"],
        background_color=pygame.Color(0, 0, 0),
        background_alpha=158,
        rel_shift=Vec2(0, 0),
        padding=100
    )

    clock: pygame.time.Clock = pygame.time.Clock()

    try:
        while True:

            try:
                frame: pygame.Surface = game.play()
            except SnakyException as exception:
                print(exception)
                break
            else:
                surface.blit(frame, (0, 0))

            if game.score > records[current_record_name]:
                records[current_record_name] = game.score

            info.update(score=game.score, record=records[current_record_name])
            pygame.draw.rect(
                surface,
                color=(89, 193, 53),
                rect=pygame.Rect(
                    info.shift.x - config["stats_border_width"],
                    info.shift.y - config["stats_border_width"],
                    config["stats_reserved_width"],
                    surface.get_size()[1]
                )
            )

            pygame.draw.rect(
                surface, color=(156, 219, 67),
                rect=pygame.Rect(
                    info.shift.x,
                    info.shift.y,
                    config["stats_reserved_width"] - config["stats_border_width"] * 2,
                    surface.get_size()[1] - config["stats_border_width"] * 2
                )
            )

            info.draw(surface)

            if game.paused or game.game_over:
                menu.draw(
                    surface,
                    msg="Game over :(" if game.game_over else "Paused",
                    score=game.score,
                    record=records[current_record_name],
                    info_lines=["Press Space to continue", "Press R to restart"]
                )


            pygame.display.update()
            clock.tick(config["tick_rate"])

    finally:

        with open(config["records_path"], "w") as w:
            json.dump(records, w)

        pygame.quit()