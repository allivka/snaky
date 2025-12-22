from .gameMap import *
import snaky.snake as snake
import random

class SnakyQuit(SnakyException):
    """Exception raised when the snake game session was quited"""
class SnakyRestart(SnakyException):
    """Exception raised when the snake game session was restarted"""

class SnakyGameOver(SnakyQuit):
    """Exception raised when attempted to play while game is over"""

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

        self.field.matrix.sync([(tile.entity.pos, True) for tile in self.snake.body])

        self.last_control_time = pygame.time.get_ticks()
        self.last_forward_time = pygame.time.get_ticks()
        self.last_tick_time = pygame.time.get_ticks()

        self.score = 0

        self.paused = False
        self.game_over = False

    def restart_game(self, config: Config | None = None) -> None:

        if config is None:
            config = self.config

        Game.__init__(self, config)

    def __str__(self) -> str:
        return f"Snake game:\n\nconfiguration={self.config}\nfield={self.field}\napple={self.apple}\nsnake={self.snake}\nsurface={self.surface}\nbody_sprites={self.body_sprites}"

    @staticmethod
    def quit() -> None:
        raise SnakyQuit("Snaky game session was quited")

    @staticmethod
    def restart() -> None:
        raise SnakyRestart

    def control_process(self, key: int) -> None:
        if pygame.time.get_ticks() - self.last_control_time < self.config["control_time_gap"]:
            return

        self.snake.direction = fix_degrees(self.snake.direction)

        dirs: dict[int, int] = {
            pygame.K_w: -90,
            pygame.K_a: 180,
            pygame.K_s: 90,
            pygame.K_d: 0,
        }

        if key not in dirs: return

        if angle_to_vec(self.snake.body[-1].direction) == -angle_to_vec(dirs[key]):
            return

        self.snake.direction = dirs[key]

        self.last_control_time = pygame.time.get_ticks()

    def pause_process(self, key: int) -> None:
        if key == pygame.K_SPACE:
            self.paused = not self.paused

    def restart_process(self, key: int) -> None:
        if key == pygame.K_r:
            self.restart()

    def keydown_process(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            raise RuntimeError(None, "event passed for keydown processing doesn't have such type")

        self.control_process(event.key)
        self.pause_process(event.key)
        self.restart_process(event.key)

    def update_state(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            match event.type:
                case pygame.QUIT: self.quit()
                case pygame.KEYDOWN:
                    self.keydown_process(event)

    def game_logic(self) -> None:
        if not (pygame.time.get_ticks() - self.last_forward_time >
                max(self.config["min_move_update_gap"], self.config["move_update_gap"] - self.config["gap_per_score"] * self.score)) or self.paused:
            return

        ready_to_eat: bool = self.snake.head.entity.pos + angle_to_vec(self.snake.direction) == self.apple.pos

        if ready_to_eat:
            self.snake.grow(1)

        self.snake.forward()
        self.snake.update()
        self.field.matrix.sync([(tile.entity.pos, True) for tile in self.snake.body if tile.tile_type != snake.TileType.head])

        if not self.field.matrix.is_valid_pos(self.snake.head.entity.pos) or self.field.matrix[self.snake.head.entity.pos]:
            self.game_over = True

        if ready_to_eat:
            self.apple.pos = random.choice(list(filter(lambda v: not bool(v[1]), self.field.matrix.unfold())))[0]
            self.score += 1

        self.last_forward_time = pygame.time.get_ticks()

    def play(self) -> pygame.Surface:

        if self.game_over:
            raise SnakyGameOver("Game was already finished. Cannot continue playing")

        if pygame.time.get_ticks() - self.last_tick_time < 1000 / self.config["tick_rate"]:
            return self.surface

        try:
            self.update_state(pygame.event.get())
            self.game_logic()
        except SnakyRestart:
            self.restart_game()

        self.surface.blit(self.field.surface, (0,0))
        self.surface.blit(self.apple.surface, self.apple.get_screen_pos())
        self.snake.draw(self.surface)

        self.last_tick_time = pygame.time.get_ticks()

        return self.surface
