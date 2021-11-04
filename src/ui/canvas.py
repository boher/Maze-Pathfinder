import pygame
import colour
from itertools import chain
from typing import Optional, Tuple
from .navbar import NavBar  # State > NavBar > Canvas > HotKeys > Instructions > Play, EventHandler init play obj
from .node import Node


class Canvas(NavBar):
    def __init__(self) -> None:
        NavBar.__init__(self)
        self.rows = 32
        self.cols = 48
        self.nav_height = 3
        self.gap = self.width // self.rows

    def create_grid(self) -> list[list[Node]]:
        grid = [[Node(row, col, self.gap, (self.rows, self.cols)) for col in range(self.cols)] for row in
                range(self.rows)]
        return grid

    def draw_grid(self) -> None:
        for row in range(self.nav_height, self.rows):
            pygame.draw.line(self.screen, colour.DARK_GREY, (0, row * self.gap), (self.length, row * self.gap))
            for col in range(self.cols):
                pygame.draw.line(self.screen, colour.DARK_GREY, (col * self.gap, (self.nav_height * self.gap)),
                                 (col * self.gap, self.width))

    def draw_canvas(self, grid: list[list[Node]]) -> None:
        self.screen.fill(colour.WHITE)
        row = chain.from_iterable(grid)
        for node in row:
            node.draw(self.screen)
        self.draw_grid()
        self.update()
        self.render(self.screen)
        pygame.display.update()

    @staticmethod
    def node_traversal(grid: list[list[Node]]) -> None:
        row = chain.from_iterable(grid)
        for node in row:
            node.update_neighbours(grid)

    @staticmethod
    def reset_open_nodes(grid: list[list[Node]]) -> None:
        row = chain.from_iterable(grid)
        for node in row:
            node.reset()

    @staticmethod
    def reset_node_visited(grid: list[list[Node]], start: Node, end: Node, bomb: Optional[Node]) -> None:
        row = chain.from_iterable(grid)
        for node in row:
            if node is not start or not end or not bomb:
                node.visited = False

    def reset_traversed_path(self, grid: list[list[Node]], start: Node, end: Node, bomb: Optional[Node]) -> None:
        self.reset_node_visited(grid, start, end, bomb)
        row = chain.from_iterable(grid)
        for node in row:
            if node.colour in (colour.BLUE, colour.TURQUOISE, colour.AQUAMARINE, colour.MAGENTA):
                node.reset()

    @staticmethod
    def reset_walls(grid: list[list[Node]]) -> None:
        row = chain.from_iterable(grid)
        for node in row:
            if node.get_wall():
                node.reset()

    def get_clicked_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        x, y = pos
        row = y // self.gap
        col = x // self.gap
        if row < self.nav_height:
            raise IndexError
        return row, col
