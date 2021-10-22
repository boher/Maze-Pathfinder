import pygame
import colour
from .button import Button
from .drop_down import DropDown
from states.state import State


class NavBar(State):
    def __init__(self) -> None:
        State.__init__(self)
        self.helper_btn = Button(10, 5, 22, 48, 10, colour.OFF_WHITE, colour.RED, "H", 20)
        self.draw_btn = Button(840, 5, 50, 48, 10, colour.BLUE_GREY, colour.BLUE, "✏", 45)
        self.erase_btn = Button(900, 5, 50, 48, 10, colour.BLUE_GREY, colour.BLUE, "❒", 45)
        self.bomb_btn = Button(720, 5, 110, 48, 10, colour.BLUE_GREY, colour.BLUE, "Add a 💣", 20)
        self.clear_options = DropDown(Button(610, 10, 100, 38, 10, colour.PURPLE, colour.BLUE, "Clear...", 15),
                                      ["Clear Path", "Clear Walls", "Clear Canvas"])
        self.speed_options = DropDown(Button(550, 10, 50, 38, 10, colour.PURPLE, colour.BLUE, "Speed", 15),
                                      ["Slow", "Default", "Fast"])
        self.visualize_btn = Button(450, 5, 90, 48, 10, colour.DARK_ORANGE, colour.ORANGE, "Visualize", 20)
        self.pathfinding_options = DropDown(Button(250, 10, 190, 38, 10, colour.PURPLE, colour.BLUE, "Pathfinding", 20),
                                            ["Dijkstra's", "A* Search", "Greedy Best-First", "Breadth-First Search",
                                             "Depth-First Search"])
        self.maze_options = DropDown(Button(42, 10, 200, 38, 10, colour.PURPLE, colour.BLUE, "Maze Generation", 20), [])
        self.nav_rect = pygame.Surface((self.length, self.width // 10.5))
        self.nav_rect.fill(colour.GREY)
        self.rect = self.nav_rect.get_rect()
        self.rect.top = 0

    def update(self) -> None:
        dropdowns = [self.pathfinding_options, self.maze_options, self.clear_options, self.speed_options]
        for dropdown in dropdowns:
            if dropdown.draw_menu and self.visualize_btn.clicked():
                dropdown.menu_active = False
                break

    def render(self, screen: pygame.surface.Surface) -> None:
        self.draw_navbar()

    def draw_navbar(self) -> None:
        self.screen.blit(self.nav_rect, self.rect)
        menu = [self.helper_btn, self.draw_btn, self.erase_btn, self.bomb_btn, self.clear_options, self.speed_options,
                self.visualize_btn, self.pathfinding_options, self.maze_options]
        for element in menu:
            element.render(self.screen)
