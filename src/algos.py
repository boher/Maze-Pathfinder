import pygame
from queue import PriorityQueue
from typing import Callable, Tuple
from ui.node import Node


class Algo:
    def __init__(self, draw: Callable, grid: list[list[Node]], start: Node, end: Node) -> None:
        self.draw = draw
        self.grid = grid
        self.start = start
        self.end = end
        self.came_from = {}
        self.heuristics = 0
        # Implemented using binary heap, get the smallest element every execution
        self.open_set = PriorityQueue()
        self.count = 0
        # Assume node is infinity distance away from compared node
        # (actual weighted path score & own est. weighted path score, since it's G(n) + H(n))
        self.g_score = {node: float("inf") for row in grid for node in row}
        self.f_score = {node: float("inf") for row in grid for node in row}

    """
    Manhattan distance heuristics
    1st param: position of start node
    2nd param: position of end node
    Return Manhattan distance between both nodes
    """
    def manhattan_dist(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
        x1, y1 = p1
        x2, y2 = p2
        self.heuristics = abs(x1 - x2) + abs(y1 - y2)
        return self.heuristics

    """
    Reconstructs optimal path found in all pathfinding algorithms by using a dict / hash map which
    indicates where each node came from, default is end node to start node
    1st param: node came from
    2nd param: current node, based on the execution step during the backtracking which starts from end node
    3rd param: nodes drawn
    No return
    """
    def optimal_path(self, came_from: dict, current: Node, draw: Callable) -> None:
        while current in came_from:
            current = came_from[current]
            current.set_path()
            draw()

    def execute(self) -> bool:
        # F(n) score of start node
        self.open_set.put((0, self.count, self.start))
        self.g_score[self.start] = 0
        self.f_score[self.start] = self.manhattan_dist(self.start.get_pos(), self.end.get_pos())
        self.start.update_neighbours(self.grid)

        # Tracking elements in priority queue by copying what the function does each step
        open_set_hash = {self.start}

        while not self.open_set.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            # Get node w/ minimum path score
            current = self.open_set.get()[2]
            # Sync w/ dequeue of current node
            open_set_hash.remove(current)

            if current == self.end:
                self.optimal_path(self.came_from, self.end, self.draw)
                self.start.set_start()
                return True

            # Neighbour nodes surrounding current node
            for neighbour in current.neighbours:

                temp_g_score = self.g_score[current] + 1

                # Estimated temp g score less than assumed g score of infinity distance,
                # then subsequently compared to the actual current g_score[neighbour]
                if temp_g_score < self.g_score[neighbour]:
                    self.came_from[neighbour] = current
                    self.g_score[neighbour] = temp_g_score
                    self.f_score[neighbour] = temp_g_score + self.manhattan_dist(neighbour.get_pos(),
                                                                                 self.end.get_pos())

                    # Sync w/ queuing of neighbour node w/ the min. weighted path score
                    if neighbour not in open_set_hash:
                        self.count += 1
                        self.open_set.put((self.f_score[neighbour], self.count, neighbour))
                        open_set_hash.add(neighbour)
                        if neighbour != self.end and not neighbour.get_end():
                            neighbour.set_open()
            self.draw()

            # Current node indicated as traversed, hence not included in open set anymore
            if current != self.start:
                current.set_closed()
        return False
