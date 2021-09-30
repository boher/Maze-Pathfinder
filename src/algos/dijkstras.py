from typing import Callable
from algos.algos import Algos
from ui.node import Node


class Dijkstras(Algos):
    """
    Dijkstra's Algorithm, weighted and guaranteed to be the shortest path
    Choosing the lowest distance node from start node by visiting all possible nodes,
    stored in a PriorityQueue until end node is found
    Once end node has been reached, backtracks using came_from dict to reconstruct the path
    1st param: Draws visualization onto canvas
    2nd param: Canvas grid being used
    3rd param: Start node
    4th param: End node
    Return: True if path found, false if no possible path
    """
    def __init__(self, draw: Callable[[], None], grid: list[list[Node]], start: Node, end: Node) -> None:
        Algos.__init__(self, draw, grid, start, end)
        self.curr_distance = 0
        # Assume node is infinity distance away from compared node
        self.distances = {node: float("inf") for row in self.grid for node in row}

    def put_open_set(self) -> None:
        # Put all surrounding lowest distance nodes
        self.open_set.put((0, self.start))
        self.distances[self.start] = 0
        self.start.update_neighbours(self.grid)

    def compare_neighbours(self, current: Node) -> None:
        # Neighbour nodes surrounding current node
        for neighbour in current.neighbours:
            # Do not traverse over neighbour nodes that are walls
            if neighbour.get_wall():
                continue

            distance = self.curr_distance + 1

            # Estimated distance of surrounding nodes less than assumed surrounding nodes of infinity distance,
            # then increment the actual current distance by 1 aft. visiting surrounding nodes
            if distance < self.distances[neighbour]:
                self.came_from[neighbour] = current
                self.curr_distance += 1
                self.distances[neighbour] = distance
                self.open_set.put((distance, neighbour))
                if neighbour != self.end and not neighbour.get_end():
                    neighbour.set_open()

    def execute(self) -> bool:
        self.put_open_set()

        while not self.open_set.empty():
            self.safe_quit()
            self.curr_distance, current = self.open_set.get()

            if current == self.end:
                self.optimal_path(self.came_from, self.end, self.draw)
                return True

            # Current distance from visited surrounding nodes compared to current node
            if self.curr_distance > self.distances[current]:
                continue

            self.compare_neighbours(current)
            self.draw()

            # Current node indicated as traversed, hence not included in open set anymore
            self.put_closed_set(current)
        return False
