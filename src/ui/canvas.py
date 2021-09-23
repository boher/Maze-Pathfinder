import pygame
import colour
from typing import Tuple
from .node import Node


class Canvas:
    def __init__(self) -> None:
        self.width = 640
        self.rows = 40
        self.gap = self.width // self.rows
        self.screen = pygame.display.set_mode((self.width, self.width), pygame.SCALED)
        pygame.display.set_caption("Maze-Pathfinder")
        pygame.font.init()

    def create_grid(self) -> list[list[Node]]:
        grid = [[Node(row, col, self.gap, self.rows) for col in range(self.rows)] for row in range(self.rows)]
        return grid

    def draw_grid(self) -> None:
        for row in range(self.rows):
            pygame.draw.line(self.screen, colour.GREY, (0, row * self.gap), (self.width, row * self.gap))
            for col in range(self.rows):
                pygame.draw.line(self.screen, colour.GREY, (col * self.gap, 0),
                                 (col * self.gap, self.width))

    def draw_canvas(self, grid: list[list[Node]]) -> None:
        self.screen.fill(colour.WHITE)
        [node.draw(self.screen) for row in grid for node in row]
        self.draw_grid()
        pygame.display.update()

    def get_clicked_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        x, y = pos
        row = y // self.gap
        col = x // self.gap
        return row, col
