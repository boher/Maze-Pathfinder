import pygame
from typing import Tuple, Union
from states.state import State


class TextObject(State):
    def __init__(self, colour: Union[pygame.Color, None], text: str = "", size: int = 0, offset: int = 0) -> None:
        State.__init__(self)
        self.colour = colour
        self.text = text
        self.size = size
        self.offset = offset

    def get_font(self) -> pygame.font.Font:
        return pygame.font.SysFont('Franklin Gothic Medium', self.size)

    def text_objects(self) -> Tuple[pygame.surface.Surface, pygame.rect.Rect]:
        text_surface = self.get_font().render(self.text, True, self.colour)
        centre_x, centre_y = self.screen.get_rect().centerx, self.screen.get_rect().centery - self.offset
        return text_surface, text_surface.get_rect(center=(centre_x, centre_y))

    def render(self, screen: pygame.surface.Surface) -> None:
        text_surf, text_rect = self.text_objects()
        self.screen.blit(text_surf, text_rect)
