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


    def __str__(self) -> str:
        return f"Snake game:\n\nconfiguration={self.config}\nfield={self.field}\napple={self.apple}\nsnake={self.snake}\nsurface={self.surface}\nbody_sprites={self.body_sprites}"

    def play(self) -> None:
        clock = pygame.time.Clock()

        start: int = pygame.time.get_ticks()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: exit()

            if pygame.time.get_ticks() - start >= 1000:
                self.snake.forward(1)
                start = pygame.time.get_ticks()

            self.surface.blit(self.field.surface, (0,0))
            self.surface.blit(self.apple.surface, self.apple.get_screen_pos())
            self.snake.draw(self.surface)

            pygame.display.update()
            clock.tick(self.config["tick_rate"])


