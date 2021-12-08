from typing import Callable, List
from algos.algos import Algos
from ui.node import Node


class GreedyBestFS(Algos):
    """
    Greedy Best-First Search Algorithm, uses greedy approach with only an admissible heuristics to find a path
    Shortest path NOT guaranteed
    Uses a priority queue with weights ignored, its evaluation function being F(n) = H(n)
    H(n) = Heuristic function (Manhattan distance from current node to end node)

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
        """Put nodes only with admissible heuristics between start node and end node"""
        self.open_set.put((self.manhattan_dist(self.start.get_pos(), self.end.get_pos()), self.start))

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
            self.open_set.put((self.manhattan_dist(neighbour.get_pos(), self.end.get_pos()), neighbour))
            if neighbour != self.end and not neighbour.get_end():
                neighbour.set_open()

    def execute(self) -> bool:
        """
        Tracking nodes in priority queue by getting untraversed node with the lowest cost

        Returns:
            True if path has been found
            False if no possible path
        """
        self.put_open_set()

        while not self.open_set.empty():
            self.safe_quit()

            current = self.open_set.get()[1]
            current.visited = True

            if current == self.end:
                self.completed_path(self.came_from, self.start, self.end, self.draw)
                return True

            current.update_nonvisited(self.grid)
            self.compare_neighbours(current)
            if not self.auto_compute:
                self.draw()

            self.put_closed_set(current)
        return False
