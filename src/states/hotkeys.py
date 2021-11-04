import pygame
import colour
from typing import Optional, Type
from ui.canvas import Canvas
from ui.node import Node
from ui.text_object import TextObject
import algos


class HotKeys(Canvas):
    def __init__(self) -> None:
        Canvas.__init__(self)
        self.start: Optional[Node] = None
        self.end: Optional[Node] = None
        self.bomb: Optional[Node] = None
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
            selected_pathfinding = self.pathfinding_keys.get(key_event)
            self.clear_path()
            self.node_traversal(self.grid)
            self.reset_node_visited(self.grid, self.start, self.end, self.bomb)
            if selected_pathfinding is not None:
                if self.bomb:
                    self.pathfind_bomb(selected_pathfinding)
                else:
                    pathfinding_algo = selected_pathfinding(lambda: self.draw_canvas(self.grid), self.grid, self.start,
                                                            self.end, self.speed, self.auto_compute)
                    self.path = pathfinding_algo.execute()
                    self.no_path_msg = pathfinding_algo.no_path() if not self.path else False
                    self.start.set_start()

    def pathfind_bomb(self, selected_pathfinding: Type[algos.Algos]) -> None:
        if self.start and self.end and self.bomb:
            start_to_bomb = selected_pathfinding(lambda: self.draw_canvas(self.grid), self.grid, self.start, self.bomb,
                                                 self.speed, self.auto_compute)
            bomb_to_end = selected_pathfinding(lambda: self.draw_canvas(self.grid), self.grid, self.bomb, self.end,
                                               self.speed, self.auto_compute)
            self.path = start_to_bomb.execute()
            self.no_path_msg = start_to_bomb.no_path() if not self.path else False
            self.reset_node_visited(self.grid, self.start, self.end, self.bomb)
            if self.path:
                self.path = bomb_to_end.execute()
                self.no_path_msg = bomb_to_end.no_path() if not self.path else False
            full_path = bomb_to_end.bomb_path + start_to_bomb.bomb_path
            if start_to_bomb.bomb_path and bomb_to_end.bomb_path:
                selected_pathfinding(lambda: self.draw_canvas(self.grid), self.grid, self.bomb, self.end, self.speed,
                                     self.auto_compute).optimal_bomb_path(lambda: self.draw_canvas(self.grid), full_path)

    def clear_open_nodes(self) -> None:
        self.auto_compute = True
        if not self.start and not self.end and not self.bomb:
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
            self.reset_traversed_path(self.grid, self.start, self.end, self.bomb)
            self.path = False

    def clear_walls(self) -> None:
        self.reset_walls(self.grid)
        self.clear_path()

    def clear_grid(self) -> None:
        self.grid = self.create_grid()
        self.bomb_btn.text = self.bomb_default_text
        self.start = None
        self.end = None
        self.bomb = None
        self.path = False
