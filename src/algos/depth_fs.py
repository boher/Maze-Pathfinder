from typing import Callable, List
from algos.algos import Algos
from ui.node import Node


class DepthFS(Algos):
    """
    Depth First Search (DFS) Algorithm, unweighted and finds a path following from the start node as deep as possible
    Uses a stack to store untraversed but visited nodes

    Args:
        draw: Draws visualizations onto canvas
        grid: Canvas grid being used
        start: Start node
        end: End node
        speed: Visualization speed
        auto-compute: Automatically compute traversed path
    """

    def __init__(self, draw: Callable[[], None], grid: List[List[Node]], start: Node, end: Node, speed: int,
                 auto_compute: bool) -> None:
        Algos.__init__(self, draw, grid, start, end, speed, auto_compute)

    def put_open_set(self) -> None:
        """Put start node as the 1st in stack and mark it as visited = True"""
        self.stack.put(self.start)
        self.start.visited = True

    def compare_neighbours(self, current: Node) -> None:
        """
        Iterates through the neighbour nodes surrounding current node, then marking them as visited
        NOTE: Neighbour nodes that are walls will not be traversed

        Args:
            current: Current node following from the start node
        """
        for neighbour in current.neighbours:
            if neighbour.get_wall():
                continue

            if not self.auto_compute:
                self.set_speed()

            neighbour.visited = True
            self.came_from[neighbour] = current
            self.stack.put(neighbour)
            if neighbour != self.end and not neighbour.get_start() and not neighbour.get_end():
                neighbour.set_open()

    def execute(self) -> bool:
        """
        Tracking nodes in stack by getting untraversed node based on LIFO principle

        Returns:
            True if path has been found
            False if no possible path
        """
        self.put_open_set()

        while not self.stack.empty():
            self.safe_quit()

            current = self.stack.get()

            if current == self.end:
                self.completed_path(self.came_from, self.start, self.end, self.draw)
                return True

            current.update_nonvisited(self.grid)
            self.compare_neighbours(current)
            if not self.auto_compute:
                self.draw()

            self.put_closed_set(current)
        return False
