import pygame
from typing import Optional
from .event_handler import EventHandler
from .instructions import Instructions
from ui.node import Node


class Play(Instructions):
    def __init__(self) -> None:
        Instructions.__init__(self)
        self.play = True
        self.pos = (0, 0)
        self.timer = 0
        self.double_click = 200
        self.hold = False
        self.erase = False
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
            self.divider()
            self.draw_canvas(self.grid)
            for event in pygame.event.get():
                EventHandler.notify(self, event)

    def state_events(self) -> None:
        while self.play:
            self.draw_canvas(self.grid)
            self.draw_btn.colour = self.draw_btn.hover_colour
            self.popup_helper()
            if not self.instructions:
                self.get_events()
