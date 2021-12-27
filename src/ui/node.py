import pygame
import colour
from typing import List, Tuple


class Node:
    def __init__(self, row: int, col: int, length: int, dimensions: Tuple[int, int]) -> None:
        self.row = row
        self.col = col
        self.length = length
        self.x = col * length
        self.y = row * length
        self.total_rows, self.total_cols = dimensions
        self.colour = colour.WHITE
        self.neighbours: List['Node'] = []
        self._visited = False

    def get_pos(self) -> Tuple[int, int]:
        """Position of node relative to canvas grid"""
        return self.row, self.col

    def get_open(self) -> bool:
        """Traversing nodes (in open set, currently looking @ them)"""
        return self.colour == colour.BLUE

    def get_closed(self) -> bool:
        """Traversed nodes (in closed set, already looked @ them)"""
        return self.colour == colour.TURQUOISE

    def get_wall(self) -> bool:
        """Construct blocking nodes (walls)"""
        return self.colour == colour.BLACK

    def get_bomb_closed(self) -> bool:
        """Traversed nodes, bomb_to_end"""
        return self.colour == colour.AQUAMARINE

    def get_start(self) -> bool:
        """Start node"""
        return self.colour == colour.GREEN

    def get_end(self) -> bool:
        """End node"""
        return self.colour == colour.RED

    def get_bomb(self) -> pygame.Color:
        """Bomb node"""
        return self.colour

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
        """
        Set bomb symbol to represent the bomb node
        NOTE: self.colour used to init bomb symbol as new class field will not draw and remove bomb
        """
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
        """
        Fills the square colour in the canvas grid
        NOTE: Bomb symbol is rendered in black, so a white square is used as its background

        Args:
            screen: Game screen
        """
        if self.get_bomb() and isinstance(self.colour, pygame.Surface):
            pygame.draw.rect(screen, colour.WHITE, (self.x, self.y, self.length, self.length))
            screen.blit(self.colour, (self.x, self.y - 1.5))
        else:
            pygame.draw.rect(screen, self.colour, (self.x, self.y, self.length, self.length))

    def update_neighbours(self, grid: List[List['Node']]) -> None:
        """
        Get neighbours of a given node, regardless if visited or not visited

        Args:
            grid: Canvas grid being used
        """
        self.neighbours = []
        # (Up) Not at row 0 and is not a wall, append previous row but same col
        if self.row > 0:
            self.neighbours.append(grid[self.row - 1][self.col])

        # (Down) Current row still within avail. total rows so that row can move down and is not a wall,
        # append next row but same col
        if self.row < self.total_rows - 1:
            self.neighbours.append(grid[self.row + 1][self.col])

        # (Left) Not at col 0 and is not a wall, append previous col but same row
        if self.col > 0:
            self.neighbours.append(grid[self.row][self.col - 1])

        # (Right) Current col still within avail. total cols so that cols can move right and is not a wall,
        # append next col but same row
        if self.col < self.total_cols - 1:
            self.neighbours.append(grid[self.row][self.col + 1])

    def update_nonvisited(self, grid: List[List['Node']]) -> None:
        """
        Get Non-visited neighbours of a given node
        NOTE: get_wall() for Dijkstra's and A*, get_visited() for Greedy Best-FS, Breadth-FS and Depth-FS

        Args:
            grid: Canvas grid being used
        """
        self.neighbours = []
        # (Up) Not at row 0 and node is untraversed, append previous row but same col
        if self.row > 0 and not grid[self.row - 1][self.col].visited:
            self.neighbours.append(grid[self.row - 1][self.col])

        # (Down) Current row still within avail. total rows so that row can move down and node is untraversed,
        # append next row but same col
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].visited:
            self.neighbours.append(grid[self.row + 1][self.col])

        # (Left) Not at col 0 and node is untraversed, append previous col but same row
        if self.col > 0 and not grid[self.row][self.col - 1].visited:
            self.neighbours.append(grid[self.row][self.col - 1])

        # (Right) Current col still within avail. total cols so that cols can move right and node is untraversed,
        # append next col but same row
        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].visited:
            self.neighbours.append(grid[self.row][self.col + 1])

    def __lt__(self, other: str) -> bool:
        return False
