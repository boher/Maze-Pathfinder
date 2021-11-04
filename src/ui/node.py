import pygame
import colour
from typing import Tuple


class Node:
    def __init__(self, row: int, col: int, length: int, dimensions: Tuple[int, int]) -> None:
        self.row = row
        self.col = col
        self.length = length
        self.x = col * length
        self.y = row * length
        self.total_rows, self.total_cols = dimensions
        self.colour = colour.WHITE
        self.neighbours: list['Node'] = []
        self._visited = False
        self.walls = [False, False, False, False]  # up, down, left, right

    def get_pos(self) -> Tuple[int, int]:
        return self.row, self.col

    def get_open(self) -> bool:
        return self.colour == colour.BLUE  # Traversing nodes (in open set, currently looking @ them)

    def get_closed(self) -> bool:
        return self.colour == colour.TURQUOISE  # Traversed nodes (in closed set, already looked @ them)

    def get_wall(self) -> bool:
        return self.colour == colour.BLACK  # Construct blocking nodes (walls)

    def get_bomb_closed(self) -> bool:
        return self.colour == colour.AQUAMARINE  # Traversed nodes, bomb_to_end

    def get_start(self) -> bool:
        return self.colour == colour.GREEN  # Start node

    def get_end(self) -> bool:
        return self.colour == colour.RED  # End node

    def btwn_wall(self, pos: int) -> bool:
        return self.walls[pos]

    def get_bomb(self) -> pygame.Color:
        return self.colour  # Bomb node

    @property
    def visited(self) -> bool:
        return self._visited

    @visited.setter
    def visited(self, visited):
        self._visited = visited

    def reset(self) -> None:
        self.colour = colour.WHITE

    def set_start(self) -> None:
        self.colour = colour.GREEN

    def set_end(self) -> None:
        self.colour = colour.RED

    def set_bomb(self) -> None:
        font = pygame.font.SysFont('SegoeUISymbol', self.length)
        text_surf = font.render("💣", True, colour.BLACK)
        self.colour = text_surf  # type: ignore

    def set_open(self) -> None:
        self.colour = colour.BLUE

    def set_closed(self) -> None:
        self.colour = colour.TURQUOISE

    def set_bomb_closed(self) -> None:
        self.colour = colour.AQUAMARINE

    def set_wall(self) -> None:
        self.colour = colour.BLACK

    def set_path(self) -> None:
        self.colour = colour.MAGENTA

    def draw(self, screen: pygame.surface.Surface) -> None:
        # self.colour used to init bomb symbol as new class field will not draw and remove bomb
        if self.get_bomb() and isinstance(self.colour, pygame.Surface):
            pygame.draw.rect(screen, colour.WHITE, (self.x, self.y, self.length, self.length))
            screen.blit(self.colour, (self.x, self.y - 1.5))
        else:
            pygame.draw.rect(screen, self.colour, (self.x, self.y, self.length, self.length))

    """
    Get neighbours from a given node, regardless if visited or not visited
    2nd param canvas: Canvas grid displayed
    Return: Traversed nodes for pathfinding
    """
    def update_neighbours(self, grid: list[list['Node']]) -> None:
        self.neighbours = []
        # (Up) Not @ row 0 & grid is not a wall (w/ cont. stmts in the algo functions), append previous row but same col
        if self.row > 0:
            self.neighbours.append(grid[self.row - 1][self.col])

        # (Down) Current row still within avail. total rows so that row can move down
        # & grid is not a wall (w/ cont. stmts in the algo functions), append next row but same col
        if self.row < self.total_rows - 1:
            self.neighbours.append(grid[self.row + 1][self.col])

        # (Left) Not @ col 0 & grid is not a wall (w/ cont. stmts in the algo functions), append previous col but same row
        if self.col > 0:
            self.neighbours.append(grid[self.row][self.col - 1])

        # (Right) Current col still within avail. total cols so that cols can move right
        # & grid is not a wall (w/ cont. stmts in the algo functions), append next col but same row
        if self.col < self.total_cols - 1:
            self.neighbours.append(grid[self.row][self.col + 1])

    """
    Get Non-visited neighbours of a given node
    2nd param: Canvas grid being used
    Return: Non-visited neighbours
    NOTE: .get_wall() for Dijkstra's & A*, get_visited() for Greedy Best-FS, Breadth-FS & Depth-FS
    """
    def update_nonvisited(self, grid: list[list['Node']]) -> None:
        self.neighbours = []
        # (Up) Not @ row 0 & node is untraversed, append previous row but same col
        if self.row > 0 and not grid[self.row - 1][self.col].visited:
            self.neighbours.append(grid[self.row - 1][self.col])

        # (Down) Current row still within avail. total rows so that row can move down
        # & node is untraversed, append next row but same col
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].visited:
            self.neighbours.append(grid[self.row + 1][self.col])

        # (Left) Not @ col 0 & node is untraversed, append previous col but same row
        if self.col > 0 and not grid[self.row][self.col - 1].visited:
            self.neighbours.append(grid[self.row][self.col - 1])

        # (Right) Current col still within avail. total cols so that cols can move right
        # & node is untraversed, append next col but same row
        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].visited:
            self.neighbours.append(grid[self.row][self.col + 1])

    def __lt__(self, other: str) -> bool:
        return False
