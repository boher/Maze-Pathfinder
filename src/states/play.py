import pygame
from random import randrange
from typing import Optional
from .event_handler import EventHandler
from .instructions import Instructions
from ui.node import Node


class Play(Instructions):
    """
    Game play state

    Attributes:
        play: A boolean indicating if game play is running
        pos: Position of mouse relative to canvas grid
        timer: An integer to track the time of the latest click
        double_click: An integer to determine if mouse click is a double-click
        hold: A boolean indicating if mouse click is being hold
        erase: A boolean indicating if erase is enabled
        drag_start: A boolean indicating if start node is being clicked and dragged
        drag_end: A boolean indicating if end node is being clicked and dragged
        drag_bomb: A boolean indicating if bomb node is being clicked and dragged
        clock: Pygame object to track time
    """

    def __init__(self) -> None:
        Instructions.__init__(self)
        self.play = True
        self.pos = (0, 0)
        self.timer = 0
        self.double_click = 200
        self.hold = False
        self.erase = False
        self.drag_start = False
        self.drag_end = False
        self.drag_bomb = False
        self.clock = pygame.time.Clock()

    def divider(self) -> None:
        """Construct a row of walls to divide the navigation bar and canvas grid"""
        for col in range(self.cols):
            divider = self.grid[self.nav_height - 1][col]
            divider.set_wall()

    def node_pos(self) -> Optional[Node]:
        """
        Get the mouse position relative to the dimensions of the canvas grid to place the node

        Returns:
            Node placed in canvas grid

        Raises:
            IndexError: If mouse position is outside the canvas grid
        """
        self.pos = pygame.mouse.get_pos()
        try:
            row, col = self.get_clicked_pos(self.pos)
            node = self.grid[row][col]
            return node
        except IndexError:
            return None

    def start_end_nodes(self, node: Node) -> None:
        """Place the start node, if start node has been set, place the end node"""
        if not self.start and node != self.end:
            self.start = node
            self.start.set_start()
        elif not self.end and node != self.start:
            self.end = node
            self.end.set_end()

    def wall_nodes(self, node: Node) -> None:
        """Construct wall nodes without drawing over start node, end node or bomb node"""
        if node != self.start and node != self.end and node != self.bomb:
            node.set_wall()

    def bomb_node(self) -> None:
        """Place the bomb node, by default in the middle of the canvas grid otherwise in a random position"""
        node = self.grid[self.rows // 2][self.cols // 2]
        while node is self.start or node is self.end or node.get_wall():
            rand_row = randrange(self.nav_height, self.rows)
            rand_col = randrange(self.nav_height, self.cols)
            node = self.grid[rand_row][rand_col]
        self.bomb = node
        self.bomb.set_bomb()

    def clear_nodes(self, node) -> None:
        """Reset placed nodes to the default"""
        node.reset()
        if node is self.start:
            self.start = None
        elif node is self.end:
            self.end = None
        elif node is self.bomb:
            self.bomb = None
            self.bomb_btn.text = self.bomb_default_text

    def get_events(self) -> None:
        """Set the canvas grid to use in game session and handle input events"""
        while self.run:
            self.clock.tick(60)
            self.divider()
            self.draw_canvas(self.grid)
            for event in pygame.event.get():
                EventHandler.notify(self, event)

    def state_events(self) -> None:
        """Set landing screen behaviour"""
        while self.play:
            self.render(self.screen)
            self.popup_helper()
            if not self.instructions:
                self.draw_btn.colour = self.draw_btn.hover_colour
                self.get_events()
