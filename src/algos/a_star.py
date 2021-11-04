from typing import Callable
from algos.algos import Algos
from ui.node import Node


class AStar(Algos):
    """
    A* Algorithm, weighted and uses calculated heuristics to find the shortest path from start node to end node efficiently
    Uses PriorityQueue with an F score, where score calculation is F(n) = G(n) + H(n)
    H = Heuristic function (Manhattan distance from current node to end node)
    G = Amount of steps taken / cost from the start node to the current node
    Basically actual weighted path score + own estimate weighted path score
    Once end node has been reached, backtracks using the came_from dict to reconstruct the path
    1st param: Draws visualizations onto canvas
    2nd param: Canvas grid being used
    3rd param: Start node
    4th param: End node
    5th param: Visualization speed
    6th param: Automatically compute traversed path
    Return: True if path is completed, false if no possible path
    """

    def __init__(self, draw: Callable[[], None], grid: list[list[Node]], start: Node, end: Node, speed: int,
                 auto_compute: bool) -> None:
        Algos.__init__(self, draw, grid, start, end, speed, auto_compute)
        self.count = 0
        self.open_set_hash: set[Node] = set()
        # Assume node is infinity distance away from compared node
        # (actual weighted path score & own est. weighted path score, since it's G(n) + H(n))
        self.g_score = {node: float("inf") for row in grid for node in row}
        self.f_score = {node: float("inf") for row in grid for node in row}

    def put_open_set(self) -> None:
        # F(n) score of start node
        self.open_set.put((0, self.count, self.start))
        self.g_score[self.start] = 0
        self.f_score[self.start] = self.manhattan_dist(self.start.get_pos(), self.end.get_pos())
        self.start.update_neighbours(self.grid)

    def compare_neighbours(self, current: Node) -> None:
        # Neighbour nodes surrounding current node
        for neighbour in current.neighbours:
            # Do not traverse over neighbour nodes that are walls
            if neighbour.get_wall():
                continue

            if not self.auto_compute:
                self.set_speed()

            temp_g_score = self.g_score[current] + 1

            # Estimated temp g score less than assumed g score of infinity distance,
            # then subsequently compared to the actual current g_score[neighbour]
            if temp_g_score < self.g_score[neighbour]:
                self.came_from[neighbour] = current
                self.g_score[neighbour] = temp_g_score
                self.f_score[neighbour] = temp_g_score + self.manhattan_dist(neighbour.get_pos(), self.end.get_pos())

                # Sync w/ queuing of neighbour node w/ the min. weighted path score
                if neighbour not in self.open_set_hash:
                    self.count += 1
                    self.open_set.put((self.f_score[neighbour], self.count, neighbour))
                    self.open_set_hash.add(neighbour)
                    if neighbour != self.end and not neighbour.get_end():
                        neighbour.set_open()

    def execute(self) -> bool:
        self.put_open_set()

        # Tracking elements in priority queue by copying what the function does each step
        self.open_set_hash = {self.start}

        while not self.open_set.empty():
            self.safe_quit()

            # Get node w/ minimum path score
            current = self.open_set.get()[2]
            # Sync w/ dequeue of current node
            self.open_set_hash.remove(current)

            if current == self.end:
                self.completed_path(self.came_from, self.start, self.end, self.draw)
                return True

            self.compare_neighbours(current)
            if not self.auto_compute:
                self.draw()

            # Current node indicated as traversed, hence not included in open set anymore
            self.put_closed_set(current)
        return False
