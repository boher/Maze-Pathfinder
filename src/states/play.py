import pygame
from typing import Optional
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

    def divider(self) -> None:
        for col in range(self.cols):
            divider = self.grid[self.nav_height - 1][col]
            divider.set_wall()

    def node_pos(self) -> Optional[Node]:
        self.pos = pygame.mouse.get_pos()
        try:
            row, col = self.get_clicked_pos(self.pos)
            node = self.grid[row][col]
            return node
        except IndexError:
            return None

    def start_end_nodes(self, node: Node) -> None:
        if not self.start and node != self.end:
            self.start = node
            self.start.set_start()
        elif not self.end and node != self.start:
            self.end = node
            self.end.set_end()

    def wall_nodes(self, node: Node) -> None:
        if node != self.start and node != self.end:
            node.set_wall()

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
            self.divider()
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
                    if event.button == 1:
                        self.hold = True
                        self.draw_erase_state()
                        if self.helper_btn.clicked():
                            self.instructions = True
                            self.popup_helper()
                if event.type == pygame.MOUSEMOTION:
                    if self.hold and node is not None:
                        if self.erase:
                            self.clear_nodes(node)
                        else:
                            self.wall_nodes(node)
                if event.type == pygame.MOUSEBUTTONUP:
                    self.hold = False
                if event.type == pygame.KEYDOWN:
                    self.pathfinding_hotkeys(event.key)
                    if event.key == pygame.K_c:
                        self.clear_grid()
                    if event.key == pygame.K_h:
                        self.instructions = True
                        self.popup_helper()

    def state_events(self) -> None:
        while self.play:
            self.draw_canvas(self.grid)
            self.draw_btn.colour = self.draw_btn.hover_colour
            self.popup_helper()
            if not self.instructions:
                self.get_events()
