import pygame
import colour
from .hotkeys import HotKeys


class Instructions(HotKeys):
    def __init__(self) -> None:
        HotKeys.__init__(self)
        self.font = pygame.font.SysFont('Franklin Gothic Medium', 24)

    def blit_newlines(self, text: str, x: int, y: int) -> None:
        newlines = text.split('\n')
        for words in newlines:
            text_surface = self.font.render(words, True, colour.BLACK)
            if text_surface.get_width() + x <= self.width:
                self.screen.blit(text_surface, (x, y))
                x += text_surface.get_width()
            else:
                y += text_surface.get_height()
                self.screen.blit(text_surface, (self.width // 9.5, y))
                x += text_surface.get_width()

    def get_instructions(self) -> str:
        return "This application visualizes various maze generation\nand pathfinding algorithms in a 2D canvas grid\n" \
               "\nLeft-click to draw a start node, then an end node\nand finally left-click and drag to draw walls\n" \
               "\nRight-click and drag to clear nodes\n" \
               "\nPress Spacebar to close instructions\n"

    def popup_helper(self) -> None:
        pygame.draw.rect(self.screen, colour.OFF_WHITE, (30, 170, 580, 300))
        # Popup helper instructions to play
        self.blit_newlines(f"INSTRUCTIONS TO PLAY\n{self.get_instructions()}\n", int(self.width // 3),
                           int(self.width // 3.5))
        pygame.display.update()
