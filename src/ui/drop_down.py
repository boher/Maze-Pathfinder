import pygame
import copy
from typing import List, Union
from .button import Button
from states.state import State


class DropDown(Button, State):
    def __init__(self, button: Button, options: List[str]) -> None:
        super().__init__(button.x, button.y, button.width, button.height, button.radius, button.colour,
                         button.hover_colour, button.text, button.size)
        State.__init__(self)
        self.rect = pygame.Rect(button.x, button.y, button.width, button.height)
        self.main = button
        self.options = options
        self.draw_menu = False
        self.menu_active = False
        self.active_option = -1

    def update(self) -> None:
        # Collapse dropdown when mouse clicks outside of options
        if not self.menu_active and self.active_option == -1:
            self.draw_menu = False

    def render(self, screen: pygame.surface.Surface) -> None:
        self.main.render(screen)
        if self.draw_menu:
            for i, text in enumerate(self.options):
                option = copy.copy(self.main)
                option.y += (i + 1) * self.rect.height
                option.text = text
                option.render(screen)

    def clicked(self) -> Union[bool, int]:
        for i, _ in enumerate(self.options):
            rect = self.rect.copy()
            rect.y += (i + 1) * self.rect.height
            if self.draw_menu and rect.collidepoint(self.main.pos):
                self.active_option = i
                break
        self.update()
        return -1
