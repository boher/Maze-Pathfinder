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
        self.algo = algos.Algo

    def pathfinding_algo(self) -> None:
        if self.start and self.end:
            self.algo(lambda: self.draw_canvas(self.grid), self.grid, self.start, self.end).execute()

    def clear_grid(self) -> None:
        self.grid = self.create_grid()
        self.start = None
        self.end = None
        self.path = False
