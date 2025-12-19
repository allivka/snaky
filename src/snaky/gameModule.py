from argparse import ArgumentError

import pygame

from .gameMap import *
import snaky.snake as snake

class Game:

    def __init__(self, config: Config) -> None:
        pygame.init()

        if not pygame.image.get_extended():
            raise NotImplementedError()

        self.config = config

        chunk : pygame.Surface = pygame.image.load(config["map_chunk_path"])
        self.field = Map(Vec2(config["map_size_x"], config["map_size_y"]), chunk)

        self.surface = pygame.display.set_mode(self.field.get_screen_size())
        pygame.display.set_caption("Snaky")
        pygame.display.set_icon(pygame.image.load(config["icon_path"]))

        self.apple = Entity(
            surface=pygame.image.load(config["apple_path"]),
            pos=Vec2(self.field.size[0] // 2, self.field.size[1] // 2),
            chunk_size=self.field.chunk_size,
            centre_shift=(config["apple_centre_shift_x"], config["apple_centre_shift_y"])
       )

        self.body_sprites = {
            snake.TileType.head: pygame.image.load(config["snake_head_path"]),
            snake.TileType.tail: pygame.image.load(config["snake_tail_path"]),
            snake.TileType.straight: pygame.image.load(config["snake_body_straight_path"]),
            snake.TileType.right: pygame.image.load(config["snake_body_blended_right_path"]),
            snake.TileType.left: pygame.transform.flip(pygame.image.load(config["snake_body_blended_right_path"]), flip_x=True, flip_y=False)
        }

        self.snake = snake.Snake(
            sprites=self.body_sprites,
            chunk_size=self.field.chunk_size,
            pos=Vec2(2, 2),
            centre_shift = (config["snake_centre_shift_x"], config["snake_centre_shift_y"]),
            direction=0,
            body_length=3
        )

        self.last_control_time = pygame.time.get_ticks()


    def __str__(self) -> str:
        return f"Snake game:\n\nconfiguration={self.config}\nfield={self.field}\napple={self.apple}\nsnake={self.snake}\nsurface={self.surface}\nbody_sprites={self.body_sprites}"

    def quit(self) -> None:
        exit()

    def control_process(self, key: int) -> None:

        if pygame.time.get_ticks() - self.last_control_time >= self.config["control_time_gap"]: return

        self.snake.direction = fix_degrees(self.snake.direction)

        dirs: dict[int, int] = {
            pygame.K_w: -90,
            pygame.K_a: 180,
            pygame.K_s: 90,
            pygame.K_d: 0,
        }

        if key not in dirs: return

        if abs(fix_degrees(self.snake.direction) - dirs[key]) == 180: return

        self.snake.direction = dirs[key]

        self.last_control_time = pygame.time.get_ticks()


    def keydown_process(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            raise RuntimeError(None, "event passed for keydown processing doesn't have such type")

        self.control_process(event.key)



    def update_state(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT: self.quit()

                case pygame.KEYDOWN:
                    self.keydown_process(event)




    def play(self) -> None:
        clock = pygame.time.Clock()

        last_forward_time: int = pygame.time.get_ticks()

        while True:
            self.update_state(pygame.event.get())

            if pygame.time.get_ticks() - last_forward_time > self.config["move_update_gap"]:
                self.snake.forward()
                last_forward_time = pygame.time.get_ticks()

            self.snake.update()

            self.surface.blit(self.field.surface, (0,0))
            self.surface.blit(self.apple.surface, self.apple.get_screen_pos())
            self.snake.draw(self.surface)

            pygame.display.update()
            clock.tick(self.config["tick_rate"])


