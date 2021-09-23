import pygame
import colour
from typing import Tuple


class Node:
    def __init__(self, row: int, col: int, length: int, total_rows: int) -> None:
        self.row = row
        self.col = col
        self.length = length
        self.x = col * length
        self.y = row * length
        self.total_rows = total_rows
        self.colour = colour.WHITE
        self.neighbours = []
        self.walls = [False, False, False, False]  # up, down, left, right

    def get_pos(self) -> Tuple[int, int]:
        return self.row, self.col

    def get_open(self) -> colour:
        return self.colour == colour.BLUE  # Traversing nodes (in open set, currently looking @ them)

    def get_closed(self) -> colour:
        return self.colour == colour.TURQUOISE  # Traversed nodes (in closed set, already looked @ them)

    def get_wall(self) -> colour:
        return self.colour == colour.BLACK  # Construct blocking nodes (walls)

    def get_start(self) -> colour:
        return self.colour == colour.GREEN  # Start node

    def get_end(self) -> colour:
        return self.colour == colour.RED  # End node

    def btwn_wall(self, pos: int) -> bool:
        return self.walls[pos]

    def reset(self) -> None:
        self.colour = colour.WHITE

    def set_start(self) -> None:
        self.colour = colour.GREEN

    def set_end(self) -> None:
        self.colour = colour.RED

    def set_open(self) -> None:
        self.colour = colour.BLUE

    def set_closed(self) -> None:
        self.colour = colour.TURQUOISE

    def set_wall(self) -> None:
        self.colour = colour.BLACK

    def set_path(self) -> None:
        self.colour = colour.MAGENTA

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.length, self.length))

    """
    Get neighbours from a given node, regardless if visited or not visited
    2nd param canvas: Canvas grid displayed
    Return: Traversed nodes for pathfinding
    """
    def update_neighbours(self, grid: list[list]) -> None:
        self.neighbours = []
        # (Up) Not @ row 0 & grid is not a wall
        if self.row > 0 and not grid[self.row - 1][self.col].get_wall():
            self.neighbours.append(grid[self.row - 1][self.col])

        # (Down) Current row still within avail. total rows so that row can move down, append next row but same col
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].get_wall():
            self.neighbours.append(grid[self.row + 1][self.col])

        # (Left) Not @ col 0 & grid is not a wall, append previous col but same row
        if self.col > 0 and not grid[self.row][self.col - 1].get_wall():
            self.neighbours.append(grid[self.row][self.col - 1])

        # (Right) Current col still within avail. total rows so that rows can move right & grid is not a wall,
        # append next col but same row
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].get_wall():
            self.neighbours.append(grid[self.row][self.col + 1])

    def __lt__(self, other: str) -> bool:
        return False