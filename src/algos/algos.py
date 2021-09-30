import pygame
from queue import PriorityQueue, LifoQueue, Queue
from typing import Any, Callable, Tuple
from ui.node import Node


class Algos:
    def __init__(self, draw: Callable[[], None], grid: list[list[Node]], start: Node, end: Node) -> None:
        self.draw = draw
        self.grid = grid
        self.start = start
        self.end = end
        self.came_from: dict[Node, Node] = {}
        self.heuristics = 0
        # Implemented using binary heap, get the smallest element every execution
        self.open_set: PriorityQueue[Any[Tuple[int, int, Node]]] = PriorityQueue()
        self.queue: Queue[Node] = Queue()
        self.stack: LifoQueue[Node] = LifoQueue()

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
    @staticmethod
    def optimal_path(came_from: dict[Node, Node], current: Node, draw: Callable[[], None]) -> None:
        while current in came_from:
            current = came_from[current]
            current.set_path()
            draw()

    @staticmethod
    def safe_quit() -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

    def put_open_set(self) -> None:
        raise NotImplementedError

    def compare_neighbours(self, current: Node) -> None:
        raise NotImplementedError

    def execute(self) -> bool:
        raise NotImplementedError

    def put_closed_set(self, current: Node) -> None:
        if current != self.start:
            current.set_closed()
