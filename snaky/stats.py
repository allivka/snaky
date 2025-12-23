from .general import *

class Stats:
    def __init__(
            self,
            font: pygame.font.Font, *,
            text_color: pygame.Color,
            current_record_name: str,
            other_records: dict[str, int],
            padding: Vec2 = Vec2(),
            shift: Vec2 = Vec2(),
            text_shift: Vec2 = Vec2(),
            ) -> None:

        self.font = font
        self.text_color = text_color
        self.padding = padding
        self.shift = shift
        self.text_shift = text_shift

        self.score = 0
        self.record = 0
        self.current_record_name = current_record_name
        self.other_records = other_records

    def update(self, *, score: int, record: int | None = None) -> None:
        self.score = score
        self.record = record if record is not None else self.record

    def draw(self, sf: pygame.Surface) -> None:
        score_text = self.font.render(f"Score: {self.score}", True, self.text_color)
        sf.blit(score_text, self.shift + self.text_shift)

        record_text = self.font.render(f"{self.current_record_name} record: {self.record}", True, self.text_color)
        sf.blit(record_text, self.shift + self.text_shift + self.padding)

        for i, name in enumerate(filter(lambda n: n != self.current_record_name, sorted(self.other_records.keys()))):
            record_text = self.font.render(f"{name} record: {self.other_records[name]}", True, self.text_color)
            sf.blit(record_text, self.shift + self.text_shift + self.padding * (i + 2))


