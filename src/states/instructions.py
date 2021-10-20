import pygame
import colour
from typing import Optional
from ui.button import Button
from .event_handler import InstructionsHandler
from .hotkeys import HotKeys


class Instructions(HotKeys):
    def __init__(self) -> None:
        HotKeys.__init__(self)
        self.close_btn = Button(720, 180, 30, 30, 10, colour.DARK_RED, colour.RED, "✖", 30)
        self.forward_btn = Button(700, 460, 50, 50, 10, colour.DARK_GREY, colour.GREY, ">", 50)
        self.back_btn = Button(210, 460, 50, 50, 10, colour.DARK_GREY, colour.GREY, "<", 50)
        self.font = pygame.font.SysFont('Franklin Gothic Medium', 24)
        self.index = 0

    def blit_newlines(self, text: str, x: int, y: int) -> None:
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

    def get_instructions(self) -> Optional[str]:
        instructions = {
            0: "This application visualizes various maze generation\n"
               "and pathfinding algorithms in a 2D canvas grid\n"
               "\nPath is calculated with Manhattan distance, an\n"
               "admissible heuristic\n"
               "\nLearn more about each algorithm after visualization\n",

            1: "Top right buttons to select between draw and erase\n"
               "Double left-click: Draw the start node, then the end\n"
               "node (required to visualize pathfinding algorithm)\n"
               "Left-click and drag: Draw walls or erase\n"
               f"{'[Z]':>25}: Clear the path\n"
               f"{'[X]':>25}: Clear the walls\n"
               f"{'[C]':>25}: Clear the canvas\n",

            2: f"{'Pathfinding':>35} Algorithms\n"
               "\nExecute via dropdown menu in navbar or hotkeys\n"
               f"{'[1]':>15}: Solve using Dijkstra's\n"
               f"{'[2]':>15}: Solve using A* Search\n"
               f"{'[3]':>15}: Solve using Greedy Best First Search\n"
               f"{'[4]':>15}: Solve using Breadth First Search\n"
               f"{'[5]':>15}: Solve using Depth First Search"
        }
        return instructions.get(self.index)

    def popup_helper(self) -> None:
        while self.instructions:
            for event in pygame.event.get():
                InstructionsHandler.notify(self, event)

            pygame.draw.rect(self.screen, colour.OFF_WHITE, (190, 170, 580, 360))
            buttons = [self.close_btn, self.forward_btn, self.back_btn]
            for button in buttons:
                button.render(self.screen)
            # Popup helper instructions to play
            self.blit_newlines(f"INSTRUCTIONS TO PLAY\n{self.get_instructions()}\n{'[H]':>25}: Open this helper again",
                               int(self.length // 2.7), int(self.width // 3.5))
            pygame.display.update()
