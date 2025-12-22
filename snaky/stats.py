from .general import *

class Stats:
    def __init__(self,
                 font: pygame.font.Font, *,
                 text_color: pygame.Color,
                 padding: Vec2 = Vec2(),
                 shift: Vec2 = Vec2(),
                 text_shift: Vec2 = Vec2()
                 ) -> None:

        self.font = font
        self.text_color = text_color
        self.padding = padding
        self.shift = shift
        self.text_shift = text_shift

        self.score = 0
        self.record = 0

    def update(self, *, score: int, record: int | None = None) -> None:
        self.score = score
        self.record = record if record is not None else self.record

    def draw(self, sf: pygame.Surface) -> None:
        score_text = self.font.render(f"Score: {self.score}", True, self.text_color)
        sf.blit(score_text, self.shift + self.text_shift)

        record_text = self.font.render(f"Record: {self.record}", True, self.text_color)
        sf.blit(record_text, self.shift + self.text_shift + self.padding)



