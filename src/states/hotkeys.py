import pygame
from typing import Optional
from ui.canvas import Canvas
from ui.node import Node
import algos


class HotKeys(Canvas):
    def __init__(self) -> None:
        Canvas.__init__(self)
        self.start: Optional[Node] = None
        self.end: Optional[Node] = None
        self.path = False
        self.grid = self.create_grid()
        self.pathfinding_keys = {
            pygame.K_1: algos.Dijkstras,
            pygame.K_2: algos.AStar,
            pygame.K_3: algos.GreedyBestFS,
            pygame.K_4: algos.BreadthFS,
            pygame.K_5: algos.DepthFS
        }

    def pathfinding_hotkeys(self, key_event) -> None:
        if key_event in self.pathfinding_keys and self.start and self.end:
            self.node_traversal(self.grid)
            self.reset_node_visited(self.grid, self.start, self.end)
            selected_pathfinding = self.pathfinding_keys.get(key_event)
            if selected_pathfinding is not None:
                selected_pathfinding(lambda: self.draw_canvas(self.grid), self.grid, self.start, self.end).execute()
                self.start.set_start()

    def clearing_keys(self, key_event: int) -> None:
        if key_event == pygame.K_c:
            self.clear_grid()

    def clear_grid(self) -> None:
        self.grid = self.create_grid()
        self.start = None
        self.end = None
        self.path = False
