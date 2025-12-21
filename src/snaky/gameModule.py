import pygame

from .gameMap import *
import snaky.snake as snake

class Game:
    def __init__(self, config: Config) -> None:
        if not pygame.image.get_extended():
            raise NotImplementedError()

        self.config = config
        self.bank = ResourceBank(config)

        chunk : pygame.Surface = self.bank.map_chunk
        self.field = Map(Vec2(config["map_size_x"], config["map_size_y"]), chunk)

        self.surface = pygame.Surface(self.field.get_screen_size())

        self.apple = Entity(
            surface=self.bank.apple,
            pos=Vec2(config["apple_start_pos"]),
            chunk_size=self.field.chunk_size,
            centre_shift=(config["apple_centre_shift_x"], config["apple_centre_shift_y"])
        )

        self.body_sprites = {
            snake.TileType.head: self.bank.snake_head,
            snake.TileType.tail: self.bank.snake_tail,
            snake.TileType.straight: self.bank.snake_body_straight,
            snake.TileType.right: self.bank.snake_body_blended_right,
            snake.TileType.left: self.bank.snake_body_blended_left,
        }

        self.snake = snake.Snake(
            sprites=self.body_sprites,
            chunk_size=self.field.chunk_size,
            pos=Vec2(config["start_pos"]),
            centre_shift = (config["snake_centre_shift_x"], config["snake_centre_shift_y"]),
            direction=config["start_direction"],
            body_length=config["start_length"]
        )

        self.last_control_time = pygame.time.get_ticks()
        self.last_forward_time = pygame.time.get_ticks()
        self.last_tick_time = pygame.time.get_ticks()

        self.paused = False

    def __str__(self) -> str:
        return f"Snake game:\n\nconfiguration={self.config}\nfield={self.field}\napple={self.apple}\nsnake={self.snake}\nsurface={self.surface}\nbody_sprites={self.body_sprites}"

    @staticmethod
    def quit() -> None:
        raise SystemExit("Game session was quited")

    def control_process(self, key: int) -> None:
        if pygame.time.get_ticks() - self.last_control_time < self.config["control_time_gap"]: return

        self.snake.direction = fix_degrees(self.snake.direction)

        dirs: dict[int, int] = {
            pygame.K_w: -90,
            pygame.K_a: 180,
            pygame.K_s: 90,
            pygame.K_d: 0,
        }

        if key not in dirs: return

        if angle_to_vec(self.snake.body[-1].direction) == -angle_to_vec(dirs[key]): return


        self.snake.direction = dirs[key]

        self.last_control_time = pygame.time.get_ticks()

    def pause_process(self, key: int) -> None:
        if key == pygame.K_SPACE:
            self.paused = not self.paused

    def keydown_process(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            raise RuntimeError(None, "event passed for keydown processing doesn't have such type")

        self.control_process(event.key)
        self.pause_process(event.key)

    def update_state(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT: self.quit()
                case pygame.KEYDOWN:
                    self.keydown_process(event)

    def menu_logic(self) -> None:
        pass

    def game_logic(self) -> None:
        if not (pygame.time.get_ticks() - self.last_forward_time > self.config["move_update_gap"]):
            return

        self.snake.forward()
        self.snake.update()

        self.last_forward_time = pygame.time.get_ticks()

    def play(self) -> pygame.Surface:

        if pygame.time.get_ticks() - self.last_tick_time < 1000 / self.config["tick_rate"]:
            return self.surface.copy()

        self.update_state(pygame.event.get())

        if self.paused:
            self.menu_logic()
        else:
            self.game_logic()

        self.surface.blit(self.field.surface, (0,0))
        self.surface.blit(self.apple.surface, self.apple.get_screen_pos())
        self.snake.draw(self.surface)

        self.last_tick_time = pygame.time.get_ticks()

        return self.surface
