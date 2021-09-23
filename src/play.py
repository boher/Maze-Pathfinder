import pygame
from hotkeys import HotKeys
from ui.node import Node


class Play(HotKeys):
    def __init__(self) -> None:
        HotKeys.__init__(self)
        self.run = True
        self.pos = None

    def node_pos(self) -> Node:
        self.pos = pygame.mouse.get_pos()
        row, col = self.get_clicked_pos(self.pos)
        node = self.grid[row][col]
        return node

    def clear_nodes(self, node) -> None:
        node.reset()
        if node is self.start:
            self.start = None
        elif node is self.end:
            self.end = None

    def get_events(self) -> None:
        while self.run:
            node = self.node_pos()
            self.draw_canvas(self.grid)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if pygame.mouse.get_pressed()[0]:
                    if not self.start and node != self.end:
                        self.start = node
                        self.start.set_start()
                    elif not self.end and node != self.start:
                        self.end = node
                        self.end.set_end()
                    elif node != self.start and node != self.end:
                        node.set_wall()
                elif pygame.mouse.get_pressed()[2]:
                    self.clear_nodes(node)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.start and self.end:
                        for row in self.grid:
                            for node in row:
                                node.update_neighbours(self.grid)
                        self.pathfinding_algo()
                    if event.key == pygame.K_c:
                        self.clear_grid()
