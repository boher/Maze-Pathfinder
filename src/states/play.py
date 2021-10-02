import pygame
from .instructions import Instructions
from ui.node import Node


class Play(Instructions):
    def __init__(self) -> None:
        Instructions.__init__(self)
        self.play = True
        self.pos = (0, 0)
        self.timer = 0
        self.double_click = 200
        self.clock = pygame.time.Clock()

    def node_pos(self) -> Node:
        self.pos = pygame.mouse.get_pos()
        row, col = self.get_clicked_pos(self.pos)
        node = self.grid[row][col]
        return node

    def start_end_nodes(self, node: Node) -> None:
        if not self.start and node != self.end:
            self.start = node
            self.start.set_start()
        elif not self.end and node != self.start:
            self.end = node
            self.end.set_end()

    def clear_nodes(self, node) -> None:
        node.reset()
        if node is self.start:
            self.start = None
        elif node is self.end:
            self.end = None

    def get_events(self) -> None:
        while self.run:
            self.clock.tick(60)
            latest_click = pygame.time.get_ticks()
            node = self.node_pos()
            self.draw_canvas(self.grid)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    self.play = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if latest_click - self.timer <= self.double_click and node is not None:
                        self.start_end_nodes(node)
                    self.timer = latest_click
                if pygame.mouse.get_pressed()[0]:
                    if node != self.start and node != self.end and node is not None:
                        node.set_wall()
                elif pygame.mouse.get_pressed()[2]:
                    self.clear_nodes(node)
                if event.type == pygame.KEYDOWN:
                    self.pathfinding_hotkeys(event.key)
                    if event.key == pygame.K_c:
                        self.clear_grid()

    def state_events(self) -> None:
        while self.play:
            self.draw_canvas(self.grid)
            self.popup_helper()
            while self.instructions:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.instructions = False
                            self.get_events()
