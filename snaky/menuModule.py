from importlib.metadata import packages_distributions

from .general import *
from dataclasses import dataclass

@dataclass(kw_only=True)
class Menu:
    size: Vec2
    shift: Vec2
    font_size: int
    font_name: str
    text_color: pygame.Color
    background_color: pygame.Color
    background_alpha: int
    rel_shift: Vec2
    padding: int

    def draw(self, sf: pygame.Surface, *, msg: str, score: int, record: int, info_lines: list[str]) -> None:

        t: pygame.Surface = pygame.Surface(self.size)
        pygame.draw.rect(t, self.background_color, pygame.Rect(self.shift.x, self.shift.y, self.size.x, self.size.y))
        t.set_alpha(self.background_alpha)
        sf.blit(t, self.shift)

        msg_text = pygame.font.SysFont(self.font_name, self.font_size).render(msg, True, self.text_color)
        sf.blit(msg_text, self.shift + self.rel_shift + Vec2(self.size.x // 2 - msg_text.get_size()[0] // 2, 0))

        score_text = pygame.font.SysFont(self.font_name, self.font_size // 2).render(
            f"Your score: {score} <-> Your record: {record}", True, self.text_color)
        sf.blit(score_text, self.shift + self.rel_shift + Vec2(self.size.x // 2 - score_text.get_size()[0] // 2,
                                                               msg_text.get_size()[1] + self.padding))

        for i, line in enumerate(info_lines):

            line_text = pygame.font.SysFont(self.font_name, self.font_size // 2).render(
                line, True, self.text_color)
            sf.blit(line_text, self.shift + self.rel_shift + Vec2(self.size.x // 2 - score_text.get_size()[0] // 2,
                                                                   msg_text.get_size()[1] + score_text.get_size()[1] + self.padding // 2 * (i + 2) + line_text.get_size()[1] * (i + 1)))
