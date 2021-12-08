import os
import pygame


class State:
    def __init__(self) -> None:
        self.run = True
        self.instructions = True
        self.length = 960
        self.width = 640
        self.screen = pygame.display.set_mode((self.length, self.width))
        self.images_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "images")
        self.icon = pygame.image.load(os.path.join(self.images_path, "icon.png")).convert_alpha()
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Maze-Pathfinder")
        pygame.font.init()

    # Abstract update state method
    def update(self) -> None:
        pass

    # Abstract render state method
    def render(self, screen: pygame.surface.Surface) -> None:
        pass
