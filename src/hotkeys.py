from ui.canvas import Canvas
import algos


class HotKeys(Canvas):
    def __init__(self) -> None:
        Canvas.__init__(self)
        self.start = None
        self.end = None
        self.path = False
        self.grid = self.create_grid()
        self.algo = algos.Algo

    def pathfinding_algo(self) -> None:
        self.algo(lambda: self.draw_canvas(self.grid), self.grid, self.start, self.end).execute()

    def clear_grid(self) -> None:
        self.grid = self.create_grid()
        self.start = None
        self.end = None
        self.path = False