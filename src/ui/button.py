import pygame
import colour
from typing import Tuple, Union
from states.state import State


class Button(State):
    def __init__(self, x: int, y: int, width: int, height: int, radius: int, colour: pygame.Color,
                 hover_colour: pygame.Color, text: str = "", size: int = 0) -> None:
        State.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius
        self.colour = colour
        self.hover_colour = hover_colour
        self.text = text
        self.size = size
        self.pos = (0, 0)

    def get_font(self) -> pygame.font.Font:
        return pygame.font.SysFont('SegoeUISymbol', self.size)

    def text_objects(self) -> Tuple[pygame.surface.Surface, pygame.rect.Rect]:
        text_surface = self.get_font().render(self.text, True, colour.BLACK)
        return text_surface, text_surface.get_rect()

    def get_text(self) -> None:
        self.get_font()
        btn_text_surf, btn_text_rect = self.text_objects()
        btn_text_rect.center = (self.x + self.width // 2, self.y + self.height // 2 - 3)
        self.screen.blit(btn_text_surf, btn_text_rect)

    def render(self, screen: pygame.surface.Surface) -> None:
        colour = self.hover_colour if Button.clicked(self) else self.colour
        pygame.draw.rect(screen, colour, (self.x, self.y, self.width, self.height), border_radius=self.radius)
        self.get_text()

    def clicked(self) -> Union[bool, int]:
        self.pos = pygame.mouse.get_pos()
        x, y = self.pos
        if (self.x <= x <= self.x + self.width) and (self.y <= y <= self.y + self.height):
            return True
        return False
