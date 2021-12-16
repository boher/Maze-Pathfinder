import os
import pygame


class State:
    """
    Abstract game state

    Attributes:
        run: A boolean indicating if application is running
        instructions: A boolean indicating if instructions is displayed
        length: Length of the Pygame screen
        width: Width of the Pygame screen
        screen: Initialize Pygame screen
        images_path: Relative path of the images directory
        icon: Load icon image
    """

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

    def update(self) -> None:
        """Abstract update state method"""
        pass

    def render(self, screen: pygame.surface.Surface) -> None:
        """Abstract render state method"""
        pass
