from typing import Callable, List
from algos.algos import Algos
from ui.node import Node


class Dijkstras(Algos):
    """
    Dijkstra's Algorithm, weighted BFS and finds the shortest path
    Uses a priority queue to store node with the lowest distance cost following from start node

    Attributes:
        curr_distance: An integer to estimate the cost to traverse to end node from current node
        distances: Estimated weighted distance of node

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
        self.curr_distance = 0
        # Assume node is infinity distance away from compared node
        self.distances = {node: float("inf") for row in self.grid for node in row}

    def put_open_set(self) -> None:
        """Put all surrounding lowest distance nodes"""
        self.open_set.put((0, self.start))
        self.distances[self.start] = 0
        self.start.update_neighbours(self.grid)

    def compare_neighbours(self, current: Node) -> None:
        """
        Iterates through the neighbour nodes surrounding current node, where its estimated distance of surrounding nodes
        should be less than assumed surrounding nodes of infinity distance
        NOTE: Neighbour nodes that are walls will not be traversed

        Args:
            current: Current node following from the start node
        """
        for neighbour in current.neighbours:
            if neighbour.get_wall():
                continue

            distance = self.curr_distance + 1
            if not self.auto_compute:
                self.set_speed()

            if distance < self.distances[neighbour]:
                self.came_from[neighbour] = current
                self.curr_distance += 1
                self.distances[neighbour] = distance
                self.open_set.put((distance, neighbour))
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
            self.curr_distance, current = self.open_set.get()

            if current == self.end:
                self.completed_path(self.came_from, self.start, self.end, self.draw)
                return True

            # To ensure distance of current node should be less than current distance from visited surrounding nodes
            if self.curr_distance > self.distances[current]:
                continue

            self.compare_neighbours(current)
            if not self.auto_compute:
                self.draw()

            self.put_closed_set(current)
        return False
