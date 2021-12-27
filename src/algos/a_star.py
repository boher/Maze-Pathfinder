from typing import Callable, List, Set
from algos.algos import Algos
from ui.node import Node


class AStar(Algos):
    """
    A* Search Algorithm, weighted and uses an admissible heuristics to find the shortest path efficiently
    Uses a priority queue with an F score, its evaluation function being F(n) = G(n) + H(n)

    Attributes:
        count: An integer to estimate the cost to traverse to end node from current node
        open_set_hash: Set list to store untraversed nodes
        g_score: Actual amount of steps taken / cost from the start node to the current node
        f_score: Evaluation function, the sum of heuristics used, the estimated weighted cost and g_score

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
        self.count = 0
        self.open_set_hash: Set[Node] = set()
        # Assume node is infinity distance away from compared node
        self.g_score = {node: float("inf") for row in grid for node in row}
        self.f_score = {node: float("inf") for row in grid for node in row}

    def put_open_set(self) -> None:
        """Set F(n) score of start node and put start node as the 1st in open set"""
        self.open_set.put((0, self.count, self.start))
        self.open_set_hash = {self.start}
        self.g_score[self.start] = 0
        self.f_score[self.start] = self.manhattan_dist(self.start.get_pos(), self.end.get_pos())
        self.start.update_neighbours(self.grid)

    def compare_neighbours(self, current: Node) -> None:
        """
        Iterates through the neighbour nodes surrounding current node, where its estimated temp g score should be less
        than assumed g score of infinity distance
        NOTE: Neighbour nodes that are walls will not be traversed

        Args:
            current: Current node following from the start node
        """
        for neighbour in current.neighbours:
            if neighbour.get_wall():
                continue

            if not self.auto_compute:
                self.set_speed()

            temp_g_score = self.g_score[current] + 1

            if temp_g_score < self.g_score[neighbour]:
                self.came_from[neighbour] = current
                self.g_score[neighbour] = temp_g_score
                self.f_score[neighbour] = temp_g_score + self.manhattan_dist(neighbour.get_pos(), self.end.get_pos())

                if neighbour not in self.open_set_hash:
                    self.count += 1
                    self.open_set.put((self.f_score[neighbour], self.count, neighbour))
                    self.open_set_hash.add(neighbour)
                    if neighbour != self.end and not neighbour.get_start() and not neighbour.get_end():
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

            current = self.open_set.get()[2]
            self.open_set_hash.remove(current)

            if current == self.end:
                self.completed_path(self.came_from, self.start, self.end, self.draw)
                return True

            self.compare_neighbours(current)
            if not self.auto_compute:
                self.draw()

            self.put_closed_set(current)
        return False
