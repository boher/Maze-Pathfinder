import random
from typing import Callable, List, Set
from algos.algos import Algos
from ui.node import Node


class RecursiveBacktracker(Algos):
    """
    Recursive Backtracker (Random DFS) Algorithm, unweighted and carves a passage following from the top left node as
    deep as possible
    Uses a stack to store untraversed wall nodes

    Attributes:
        random_neighbour: Random neighbour node
        open_set_hash: Set list to store untraversed wall nodes

    Args:
        draw: Draws visualizations onto canvas
        grid: Canvas grid being used
        start: Start node, which is the top left node
        end: End node, which is the top left node
        speed: Visualization speed
        auto-compute: Automatically compute traversed path
    """

    def __init__(self, draw: Callable[[], None], grid: List[List[Node]], start: Node, end: Node, speed: int,
                 auto_compute: bool) -> None:
        Algos.__init__(self, draw, grid, start, end, speed, auto_compute)
        self.random_neighbour = None
        self.open_set_hash: Set[Node] = set()

    def put_open_set(self) -> None:
        """Put top left node of grid as the 1st in stack and open set"""
        top_left_node = self.start
        self.open_set_hash = {top_left_node}
        self.stack.put(top_left_node)

    def compare_neighbours(self, current: Node) -> None:
        """
        Iterates through the neighbour nodes surrounding current node, where a random neighbour is chosen from the
        filtered list of current neighbours

        Args:
            current: Current node following from the top left node
        """
        neighbours = [neighbour for neighbour in current.neighbours if neighbour not in self.open_set_hash and
                      neighbour.row >= self.start.row]
        if neighbours:
            self.random_neighbour = random.choice(neighbours)
            self.random_neighbour.set_open()

            if not self.auto_compute:
                self.set_speed()

            for neighbour in neighbours:
                self.open_set_hash.add(neighbour)

                if neighbour != self.random_neighbour:
                    self.stack.put(neighbour)

            self.stack.put(self.random_neighbour)
            if current != self.start and current != self.end and not self.is_bomb(current):
                current.reset()

    def execute(self) -> bool:
        """
        Tracking nodes in stack by getting untraversed wall node based on LIFO principle

        Returns:
            True upon successful maze generation
        """
        self.put_open_set()

        while not self.stack.empty():
            self.safe_quit()
            current = self.stack.get()
            self.compare_neighbours(current)
            if not self.auto_compute:
                self.draw()
            self.random_neighbour.reset()
        return True
