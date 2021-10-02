import pygame
import colour
from ui.button import Button
from .hotkeys import HotKeys


class Instructions(HotKeys):
    def __init__(self) -> None:
        HotKeys.__init__(self)
        self.close_btn = Button(720, 180, 30, 30, 10, colour.DARK_RED, colour.RED, "✖", 30)
        self.font = pygame.font.SysFont('Franklin Gothic Medium', 24)

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

    def get_instructions(self) -> str:
        return "This application visualizes various maze generation\nand pathfinding algorithms in a 2D canvas grid\n" \
               "\nTop right buttons to select between draw and erase\n" \
               "\nDouble left-click to draw a start node, then an end\n" \
               "node (required to visualize pathfinding algorithm)\n" \
               "Left-click and drag: Draw walls or erase\n"

    def popup_helper(self) -> None:
        while self.instructions:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.close_btn.clicked():
                        self.instructions = False
                pygame.draw.rect(self.screen, colour.OFF_WHITE, (190, 170, 580, 360))
                self.close_btn.render(self.screen)
                # Popup helper instructions to play
                self.blit_newlines(f"INSTRUCTIONS TO PLAY\n{self.get_instructions()}\n{'[H]':>25}: Open this helper again",
                                   int(self.length // 2.7), int(self.width // 3.5))
            pygame.display.update()
