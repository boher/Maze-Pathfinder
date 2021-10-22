from typing import Callable
from algos.algos import Algos
from ui.node import Node


class BreadthFS(Algos):
    """
    BFS Algorithm, unweighted and guaranteed to be the shortest path
    Uses a queue to store nodes since BFS is unweighted
    Once end node has been reached, backtracks using the came_from dict to reconstruct the path
    1st param: Draws visualizations onto canvas
    2nd param: Canvas grid being used
    3rd param: Start node
    4th param: End node
    Return: True if path is completed, false if no possible path
    """

    def __init__(self, draw: Callable[[], None], grid: list[list[Node]], start: Node, end: Node, speed: int) -> None:
        Algos.__init__(self, draw, grid, start, end, speed)

    def put_open_set(self) -> None:
        # Put all surrounding nodes
        self.queue.put(self.start)
        # Mark start node as visited = True, since it would always be the 1st node placed in queue
        self.start.visited = True

    def compare_neighbours(self, current: Node) -> None:
        # Neighbour nodes surrounding current node
        for neighbour in current.neighbours:
            # Do not traverse over neighbour nodes that are walls
            if neighbour.get_wall():
                continue

            self.set_speed()

            # Mark neighbour node visited as True, then subsequently compared to the current node,
            # which will put any surrounding unvisited neighbours
            neighbour.visited = True
            self.came_from[neighbour] = current
            self.queue.put(neighbour)
            if neighbour != self.end and not neighbour.get_end():
                neighbour.set_open()

    def execute(self) -> bool:
        self.put_open_set()

        while not self.queue.empty():
            self.safe_quit()

            # Get node based on FIFO
            current = self.queue.get()

            if current == self.end:
                self.optimal_path(self.came_from, self.end, self.draw)
                return True

            current.update_nonvisited(self.grid)
            self.compare_neighbours(current)
            self.draw()

            # Current node indicated as traversed, hence not included in open set
            self.put_closed_set(current)
        return False
