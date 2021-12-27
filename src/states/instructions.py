import pygame
import colour
from typing import Optional
from ui.button import Button
from ui.text_object import TextObject
from .instructions_handler import InstructionsHandler
from .hotkeys import HotKeys


class Instructions(HotKeys):
    """
    Game instructions state, provides user a guide on how to interact with the application
    Provides learning resources for more information on an algorithm not defined in game

    Attributes:
        close_btn: Button element for user to close the instructions
        forward_btn: Button element for user to navigate to the next page in instructions
        back_btn: Button element for user to navigate to the previous page in instructions
        visualgo_resource: Button element for user to access the VisuAlgo resource
        handson_resource: Button element for user to access handson resource for either maze generation or pathfinding algorithm
        github_repo: Button element for user to access the GitHub repository of the source code
        font: Set the font type used in instructions text
        index: An integer of the current page to display in instructions
    """

    def __init__(self) -> None:
        HotKeys.__init__(self)
        self.close_btn = Button(720, 180, 30, 30, 10, colour.DARK_RED, colour.RED, "✖", 30)
        self.forward_btn = Button(700, 460, 50, 50, 10, colour.DARK_GREY, colour.GREY, ">", 50)
        self.back_btn = Button(210, 460, 50, 50, 10, colour.DARK_GREY, colour.GREY, "<", 50)
        self.visualgo_resource = Button(360, 268, 240, 55, 10, colour.DARK_GREY, colour.GREY, "", 0)
        self.handson_resource = Button(350, 350, 260, 55, 10, colour.DARK_GREY, colour.GREY, "", 0)
        self.github_repo = Button(210, 350, 190, 30, 10, colour.DARK_GREY, colour.GREY, "", 0)
        self.font = TextObject(colour.BLACK, "", 24, 0).get_font()
        self.index = 0

    def blit_newlines(self, text: str, x: int, y: int) -> None:
        """Format text to newline to fit within popup helper"""
        newlines = text.split('\n')
        for words in newlines:
            text_surface = self.font.render(words, True, colour.BLACK)
            if text_surface.get_width() + x <= self.length:
                self.screen.blit(text_surface, (x, y))
                x += text_surface.get_width()
            else:
                y += text_surface.get_height()
                self.screen.blit(text_surface, (self.length // 4.5, y))
                x += text_surface.get_width()

    def get_handson_resource_text(self) -> str:
        """Different resources for maze generation and pathfinding algorithms"""
        if self.path:
            handson_resource_text = f"\n{'Pathfinding:':>38} Red Blob\n" \
                                    f"{'Games':>31} by Amit Patel\n"
        else:
            handson_resource_text = f"\n{'Mazes':>29} for Programmers\n" \
                                    f"{'by':>35} Jamis Buck\n"
        return handson_resource_text

    def get_learn_more(self) -> str:
        """Display learn more instructions based on visualization state"""
        if self.index == 3:
            if (self.maze_options.active_option > -1 and self.maze) or (self.pathfinding_options.active_option > -1 and
                                                                        self.path):
                self.visualgo_resource.render(self.screen)
                self.handson_resource.render(self.screen)
                active_option = self.pathfinding_options.options[self.pathfinding_options.active_option] \
                    if self.path else self.maze_options.options[self.maze_options.active_option]
                return f"{'Here are some resources to learn more about the':>25}\n" \
                       f"{active_option} algorithm\n" \
                       f"{'Algorithm':>35} explanation\n" \
                       f"{'lectures':>35} by VisuAlgo\n" + self.get_handson_resource_text()
            else:
                self.github_repo.render(self.screen)
        return "Thank you for browsing through the instructions\n" \
               "\nClose the popup helper here for easy access to\n" \
               "learn more about the latest algorithm visualized\n" \
               "\nGo to source code\n" \
               "MIT License\n"

    def get_instructions(self) -> Optional[str]:
        """Get instructions based on the current page index"""
        instructions = {
            0: "This application visualizes various maze generation\n"
               "and pathfinding algorithms in a 2D canvas grid\n"
               "\nPath is calculated with Manhattan distance, an\n"
               "admissible heuristic\n"
               "\nLearn more about each algorithm after visualization\n",

            1: "Top right buttons to select between draw and erase\n"
               "Double left-click: Draw the start node, then the end\n"
               "node (required to visualize pathfinding algorithm)\n"
               "Left-click and drag: Move nodes, draw walls or erase\n"
               "Bomb: Pathfinding algorithm will find the bomb first\n"
               f"{'[Z]':>25}: Clear the path\n"
               f"{'[X]':>25}: Clear the walls\n"
               f"{'[C]':>25}: Clear the canvas",

            2: f"{'Pathfinding':>35} Algorithms\n"
               "\nExecute via dropdown menu in navbar or hotkeys\n"
               f"{'[1]':>15}: Solve using Dijkstra's\n"
               f"{'[2]':>15}: Solve using A* Search\n"
               f"{'[3]':>15}: Solve using Greedy Best First Search\n"
               f"{'[4]':>15}: Solve using Breadth First Search\n"
               f"{'[5]':>15}: Solve using Depth First Search",

            3: self.get_learn_more()
        }
        return instructions.get(self.index)

    def popup_helper(self) -> None:
        """Display instructions over canvas grid"""
        while self.instructions:
            for event in pygame.event.get():
                InstructionsHandler.notify(self, event)

            pygame.draw.rect(self.screen, colour.OFF_WHITE, (190, 170, 580, 360))
            buttons = [self.close_btn, self.forward_btn, self.back_btn]
            for button in buttons:
                button.render(self.screen)
            self.blit_newlines(f"INSTRUCTIONS TO PLAY\n{self.get_instructions()}\n{'[H]':>25}: Open this helper again",
                               int(self.length // 2.7), int(self.width // 3.5))
            pygame.display.update()
