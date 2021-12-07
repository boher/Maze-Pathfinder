from typing import Callable, List
from algos.algos import Algos
from ui.node import Node


class GreedyBestFS(Algos):
    """
    Weighted DFS/BFS algorithm, using greedy approach to find a path from start to the end node. Shortest path NOT guaranteed
    Uses a priority queue and calculated heuristics (Manhattan distance) to choose which node it will visit next
    Once end node has been reached, backtracks using the came_from dict to reconstruct the path
    1st param: Draws visualizations onto canvas
    2nd param: Canvas grid being used
    3rd param: Start node
    4th param: End node
    5th param: Visualization speed
    6th param: Automatically compute traversed path
    Return: True if path is completed, false if no possible path
    """
    def __init__(self, draw: Callable[[], None], grid: List[List[Node]], start: Node, end: Node, speed: int,
                 auto_compute: bool) -> None:
        Algos.__init__(self, draw, grid, start, end, speed, auto_compute)

    def put_open_set(self) -> None:
        # Put nodes only w/ ideal calculated heuristics between start node and end node
        self.open_set.put((self.manhattan_dist(self.start.get_pos(), self.end.get_pos()), self.start))

    def compare_neighbours(self, current: Node) -> None:
        # Neighbour nodes surrounding current node
        for neighbour in current.neighbours:
            # Do not traverse over neighbour nodes that are walls
            if neighbour.get_wall():
                continue

            if not self.auto_compute:
                self.set_speed()

            # Mark neighbour node visited as True, then subsequently compared to the current node,
            # which will only put nodes with the ideal calculated heuristics
            neighbour.visited = True
            self.came_from[neighbour] = current
            self.open_set.put((self.manhattan_dist(neighbour.get_pos(), self.end.get_pos()), neighbour))
            if neighbour != self.end and not neighbour.get_end():
                neighbour.set_open()

    def execute(self) -> bool:
        self.put_open_set()

        while not self.open_set.empty():
            self.safe_quit()

            # Get minimum path score node
            current = self.open_set.get()[1]
            current.visited = True

            if current == self.end:
                self.completed_path(self.came_from, self.start, self.end, self.draw)
                return True

            current.update_nonvisited(self.grid)
            self.compare_neighbours(current)
            if not self.auto_compute:
                self.draw()

            # Current node indicated as traversed, hence not included in open set anymore
            self.put_closed_set(current)
        return False
