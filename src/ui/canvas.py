import pygame
import colour
from itertools import chain
from typing import Tuple
from states.state import State
from .node import Node


class Canvas(State):
    def __init__(self) -> None:
        State.__init__(self)
        self.width = 640
        self.rows = 40
        self.gap = self.width // self.rows

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
        row = chain.from_iterable(grid)
        for node in row:
            node.draw(self.screen)
        self.draw_grid()
        pygame.display.update()

    @staticmethod
    def node_traversal(grid: list[list[Node]]) -> None:
        row = chain.from_iterable(grid)
        for node in row:
            node.update_neighbours(grid)

    @staticmethod
    def reset_node_visited(grid: list[list[Node]], start: Node, end: Node):
        def set_node_unvisited(node):
            node.visited = False
        row = chain.from_iterable(grid)
        for node in row:
            if node is not start or not end:
                set_node_unvisited(node)

    def get_clicked_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        x, y = pos
        row = y // self.gap
        col = x // self.gap
        return row, col
