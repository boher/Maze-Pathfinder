import pygame
import colour
from typing import Optional
from ui.canvas import Canvas
from ui.node import Node
from ui.text_object import TextObject
import algos


class HotKeys(Canvas):
    def __init__(self) -> None:
        Canvas.__init__(self)
        self.start: Optional[Node] = None
        self.end: Optional[Node] = None
        self.path = False
        self.no_path_msg = False
        self.no_start_end_msg = False
        self.auto_compute = False
        self.speed = 0
        self.grid = self.create_grid()
        self.pathfinding_keys = {
            pygame.K_1: algos.Dijkstras,
            pygame.K_2: algos.AStar,
            pygame.K_3: algos.GreedyBestFS,
            pygame.K_4: algos.BreadthFS,
            pygame.K_5: algos.DepthFS
        }

    def update(self) -> None:
        if self.no_path_msg:
            no_path = TextObject(colour.RED, "No path found", 40, self.width // self.cols)
            no_path.render(self.screen)
        if self.no_start_end_msg:
            no_start_end = TextObject(colour.ORANGE, "Please set the start and end node to visualize pathfinding "
                                                     "algorithm", self.rows, self.width // self.cols)
            no_start_end.render(self.screen)

    def pathfinding_hotkeys(self, key_event) -> None:
        if key_event in self.pathfinding_keys and self.start and self.end:
            self.clear_path()
            self.node_traversal(self.grid)
            self.reset_node_visited(self.grid, self.start, self.end)
            selected_pathfinding = self.pathfinding_keys.get(key_event)
            if selected_pathfinding is not None:
                pathfinding_algo = selected_pathfinding(lambda: self.draw_canvas(self.grid), self.grid, self.start,
                                                        self.end, self.speed, self.auto_compute)
                self.path = pathfinding_algo.execute()
                self.no_path_msg = pathfinding_algo.no_path() if not self.path else False
                self.start.set_start()

    def clear_open_nodes(self) -> None:
        self.auto_compute = True
        if not self.start and not self.end:
            self.reset_open_nodes(self.grid)

    def clearing_keys(self, key_event: int) -> None:
        if key_event == pygame.K_z:
            self.clear_path()
        if key_event == pygame.K_x:
            self.clear_walls()
        if key_event == pygame.K_c:
            self.clear_grid()

    def clear_path(self) -> None:
        if self.start and self.end:
            self.reset_traversed_path(self.grid, self.start, self.end)
            self.path = False

    def clear_walls(self) -> None:
        self.reset_walls(self.grid)
        self.clear_path()

    def clear_grid(self) -> None:
        self.grid = self.create_grid()
        self.start = None
        self.end = None
        self.path = False
