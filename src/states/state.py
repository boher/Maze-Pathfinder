import pygame


class State:
    def __init__(self) -> None:
        self.run = True
        self.instructions = True
        self.length = 960
        self.width = 640
        self.screen = pygame.display.set_mode((self.length, self.width), pygame.SCALED)
        pygame.display.set_caption("Maze-Pathfinder")
        pygame.font.init()

    # Abstract update state method
    def update(self) -> None:
        pass

    # Abstract render state method
    def render(self, screen: pygame.surface.Surface) -> None:
        pass
