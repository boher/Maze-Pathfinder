import pygame
from queue import PriorityQueue, LifoQueue, Queue
from typing import Any, Callable, Dict, List, Tuple
from ui.node import Node


class Algos:
    """
    Parent class for algorithm to inherit common methods

    Attributes:
        draw: Draws visualizations onto canvas
        grid: Canvas grid being used
        start: Start node
        end: End node
        speed: Visualization speed
        auto_compute: Automatically compute traversed path
        came_from: Dictionary of nodes, indicating node came from, backtracking from the end node
        heuristics: An integer of the calculated heuristics
        bomb_path: A list of nodes resolving to and from the bomb node
        open_set: Priority queue instance
        queue: Queue instance
        stack: LIFO queue instance
    """

    def __init__(self, draw: Callable[[], None], grid: List[List[Node]], start: Node, end: Node, speed: int,
                 auto_compute: bool) -> None:
        self.draw = draw
        self.grid = grid
        self.start = start
        self.end = end
        self.speed = speed
        self.auto_compute = auto_compute
        self.came_from: Dict[Node, Node] = {}
        self.heuristics = 0
        self.bomb_path: List[Node] = []
        # Implemented using binary heap, get the smallest element every execution
        self.open_set: PriorityQueue[Any[Tuple[int, int, Node]]] = PriorityQueue()
        self.queue: Queue[Node] = Queue()
        self.stack: LifoQueue[Node] = LifoQueue()

    def set_speed(self) -> None:
        """Used to set speed of algorithm visualization"""
        pygame.time.delay(self.speed)

    def manhattan_dist(self, p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
        """
        Manhattan distance heuristics

        Args:
            p1: Position of start or neighbour node
            p2: Position of end node

        Returns:
            Manhattan distance between both nodes
        """
        x1, y1 = p1
        x2, y2 = p2
        self.heuristics = abs(x1 - x2) + abs(y1 - y2)
        return self.heuristics

    def optimal_path(self, came_from: Dict[Node, Node], current: Node, draw: Callable[[], None]) -> None:
        """
        Reconstructs optimal path found in all pathfinding algorithms by using a dict / hash map which indicates where
        each node came from, reconstructs path from end node to start node

        Args:
            came_from: Node came from, backtracking from the end node
            current: Current node
            draw: Draws visualizations onto canvas
        """
        while current in came_from:
            current = came_from[current]
            current.set_path()
            if not self.auto_compute:
                self.set_speed()
                draw()

    def append_bomb_path(self, came_from: Dict[Node, Node], current: Node) -> None:
        """
        Append nodes backtracked in came_from dict to create start node to bomb node path and bomb node to end node path

        Args:
            came_from: Node came from, backtracking from the end node
            current: Current node
        """
        while current in came_from:
            current = came_from[current]
            self.bomb_path.append(current)

    def optimal_bomb_path(self, draw: Callable[[], None], full_path: List[Node]) -> None:
        """
        Once end node has been reached, backtracks using the full_path list of nodes to reconstruct the path

        Args:
            draw: Draws visualizations onto canvas
            full_path: Concatenated start node to bomb node path and bomb node to end node path
        """
        for current in full_path:
            if not current.get_start() and not current.get_end() and not self.is_bomb(current):
                current.set_path()
                if not self.auto_compute:
                    self.set_speed()
                    draw()

    def completed_path(self, came_from: Dict[Node, Node], start: Node, end: Node, draw: Callable[[], None]) -> None:
        """
        Once end node has been reached, backtracks using the came_from dict to reconstruct the path

        Args:
            came_from: Node came from, backtracking from the end node
            start: Start node
            end: End node
            draw: Draws visualizations onto canvas
        """
        if self.is_bomb(self.start) or self.is_bomb(self.end):
            self.append_bomb_path(came_from, end)
        else:
            self.optimal_path(came_from, end, draw)
            start.set_start()

    @staticmethod
    def is_bomb(node: Node) -> bool:
        """Only bomb node has colour property of Surface type"""
        if isinstance(node.colour, pygame.Surface):
            return True
        else:
            return False

    @staticmethod
    def no_path() -> bool:
        """Used to set no path message"""
        return True

    @staticmethod
    def safe_quit() -> None:
        """Safe quit game if algorithm is still being executed"""
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
        """
        Current node indicated as traversed, hence not included in open set anymore

        Args:
            current: Current node following from the start node
        """
        if current != self.start and not current.get_end():
            if self.is_bomb(self.start):
                current.set_bomb_closed() if not current.get_start() else None
            else:
                current.set_closed()
