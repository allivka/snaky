from .gameMap import *
import snake

class Game:

    def __init__(self, config: Config) -> None:
        pygame.init()

        if not pygame.image.get_extended():
            raise NotImplementedError()

        self.config = config

        chunk : pygame.Surface = pygame.image.load(config["map_chunk_path"])
        self.field = Map((config["map_size_x"], config["map_size_y"]), chunk)

        self.surface = pygame.display.set_mode(self.field.get_screen_size())
        pygame.display.set_caption("Snaky")
        pygame.display.set_icon(pygame.image.load(config["icon_path"]))

        self.apple = Entity(surface=pygame.image.load(config["apple_path"]),
                           pos=(self.field.size[0] // 2, self.field.size[1] // 2),
                           chunk_size=self.field.chunk_size,
                           centre_shift=(config["apple_centre_shift_x"], config["apple_centre_shift_y"])
                           )

        self.snake = snake.Snake()



    def play(self) -> None:
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: exit()

            self.surface.blit(self.field.surface, (0,0))
            self.surface.blit(self.apple.surface, self.apple.get_screen_pos())

            pygame.display.update()
            clock.tick(self.config["tick_rate"])

