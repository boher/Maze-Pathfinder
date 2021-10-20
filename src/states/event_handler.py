import pygame
import colour
from typing import Callable, Dict, TYPE_CHECKING, TypeVar, Union

if TYPE_CHECKING:  # Avoid circular imports
    from .instructions import Instructions
    from .play import Play


class InstructionsHandler:
    R = TypeVar("R")
    instructions_registry: Dict[
        Union[int, list[Callable[..., 'Instructions']]], list[Callable[..., pygame.event.Event]]] = {}

    @staticmethod
    def register(event_type: int) -> Callable[..., R]:
        def decorator(func):
            InstructionsHandler.instructions_registry.setdefault(event_type, []).append(func)

        return decorator

    @staticmethod
    def notify(instructions: 'Instructions', event: pygame.event.Event) -> None:
        func_loop = InstructionsHandler.instructions_registry[
            event.type] if event.type in InstructionsHandler.instructions_registry else []
        for func in func_loop:
            func(instructions, event)


@InstructionsHandler.register(pygame.QUIT)
def instructions_quit(*_) -> None:
    pygame.quit()
    exit()


@InstructionsHandler.register(pygame.MOUSEBUTTONDOWN)
def helper_click_actions(instructions: 'Instructions', event: pygame.event.Event) -> None:
    left_button = 1
    close_btn = instructions.close_btn
    forward_btn = instructions.forward_btn
    back_btn = instructions.back_btn
    if event.button == left_button:
        instructions.hold = True
        if close_btn.clicked():
            instructions.instructions = False
        if forward_btn.clicked():
            while instructions.index < 2:
                instructions.index += 1
                break
        if back_btn.clicked():
            while instructions.index > 0:
                instructions.index -= 1
                break


class EventHandler:
    R = TypeVar("R")
    event_handler_registry: Dict[Union[int, list[Callable[..., 'Play']]], list[Callable[..., pygame.event.Event]]] = {}

    @staticmethod
    def register(event_type: int) -> Callable[..., R]:
        def decorator(func):
            EventHandler.event_handler_registry.setdefault(event_type, []).append(func)

        return decorator

    @staticmethod
    def notify(play_obj: 'Play', event: pygame.event.Event) -> None:
        func_loop = EventHandler.event_handler_registry[
            event.type] if event.type in EventHandler.event_handler_registry else []
        for func in func_loop:
            func(play_obj, event)


@EventHandler.register(pygame.QUIT)
def safe_quit(play_obj: 'Play', *_) -> None:
    play_obj.run = False
    play_obj.play = False
    pygame.quit()
    exit()


@EventHandler.register(pygame.MOUSEBUTTONDOWN)
def helper_state(play_obj: 'Play', event: pygame.event.Event) -> None:
    left_button = 1
    helper_btn = play_obj.helper_btn
    if event.button == left_button and helper_btn.clicked():
        play_obj.hold = True
        play_obj.instructions = True
        play_obj.popup_helper()


@EventHandler.register(pygame.MOUSEBUTTONDOWN)
def double_left_click(play_obj: 'Play', event: pygame.event.Event) -> None:
    left_button = 1
    node = play_obj.node_pos()
    latest_click = pygame.time.get_ticks()
    if event.button == left_button and node is not None:
        if latest_click - play_obj.timer <= play_obj.double_click:
            play_obj.start_end_nodes(node)
        play_obj.timer = latest_click


@EventHandler.register(pygame.MOUSEMOTION)
def click_drag(play_obj: 'Play', *_) -> None:
    node = play_obj.node_pos()
    if play_obj.hold and node is not None:
        if play_obj.erase:
            play_obj.clear_nodes(node)
        else:
            play_obj.wall_nodes(node)


@EventHandler.register(pygame.MOUSEBUTTONUP)
def stop_click_drag(play_obj: 'Play', *_) -> None:
    play_obj.hold = False


@EventHandler.register(pygame.KEYDOWN)
def hot_key_down(play_obj: 'Play', event: pygame.event.Event) -> None:
    if event.key == pygame.K_h:
        play_obj.instructions = True
        play_obj.popup_helper()
    play_obj.pathfinding_hotkeys(event.key)
    play_obj.clearing_keys(event.key)


@EventHandler.register(pygame.MOUSEBUTTONDOWN)
def draw_state(play_obj: 'Play', event: pygame.event.Event) -> None:
    left_button = 1
    draw_btn = play_obj.draw_btn
    erase_btn = play_obj.erase_btn
    if event.button == left_button:
        play_obj.hold = True
        if draw_btn.clicked():
            play_obj.erase = False
            draw_btn.colour, erase_btn.colour = erase_btn.hover_colour, colour.BLUE_GREY
        if erase_btn.clicked():
            play_obj.erase = True
            erase_btn.colour, draw_btn.colour = erase_btn.hover_colour, colour.BLUE_GREY
