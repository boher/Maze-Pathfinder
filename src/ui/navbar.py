import pygame
import colour
from .button import Button
from states.state import State


class NavBar(State):
    def __init__(self) -> None:
        State.__init__(self)
        self.helper_btn = Button(10, 5, 22, 48, 10, colour.OFF_WHITE, colour.RED, "H", 20)
        self.draw_btn = Button(840, 5, 50, 48, 10, colour.BLUE_GREY, colour.BLUE, "✏", 45)
        self.erase_btn = Button(900, 5, 50, 48, 10, colour.BLUE_GREY, colour.BLUE, "❒", 45)
        self.nav_rect = pygame.Surface((self.length, self.width // 10.5))
        self.nav_rect.fill(colour.GREY)
        self.rect = self.nav_rect.get_rect()
        self.rect.top = 0

    def update(self) -> None:
        pass

    def render(self, screen: pygame.surface.Surface) -> None:
        self.draw_navbar()

    def draw_navbar(self) -> None:
        self.screen.blit(self.nav_rect, self.rect)
        menu = [self.helper_btn, self.draw_btn, self.erase_btn]
        for element in menu:
            element.render(self.screen)
