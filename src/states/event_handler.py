import pygame
import colour
from typing import Callable, Dict, TYPE_CHECKING, TypeVar, Union

if TYPE_CHECKING:  # Avoid circular imports
    from .instructions import Instructions
    from .play import Play
    from ui.button import Button
    from ui.drop_down import DropDown

# Since pygame keys are integer constants
PATHFINDING_KEY_OFFSET = 49


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
        if close_btn.clicked():
            instructions.instructions = False
            instructions.speed = 15
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


@EventHandler.register(pygame.MOUSEMOTION)
def dismiss_text(play_obj: 'Play', *_) -> None:
    if play_obj.no_path_msg:
        play_obj.no_path_msg = False
    if play_obj.no_start_end_msg:
        play_obj.no_start_end_msg = False


@EventHandler.register(pygame.KEYDOWN)
def hot_key_down(play_obj: 'Play', event: pygame.event.Event) -> None:
    play_obj.no_path_msg = False
    play_obj.pathfinding_options.draw_menu = False
    if event.key == pygame.K_h:
        play_obj.instructions = True
        play_obj.popup_helper()
    hot_key_visualize(play_obj, event)
    play_obj.clearing_keys(event.key)


@EventHandler.register(pygame.MOUSEBUTTONDOWN)
def draw_state(play_obj: 'Play', event: pygame.event.Event) -> None:
    left_button = 1
    draw_btn = play_obj.draw_btn
    erase_btn = play_obj.erase_btn
    visualize_btn = play_obj.visualize_btn
    if event.button == left_button and not visualize_btn.clicked():
        play_obj.hold = True
        if draw_btn.clicked():
            play_obj.erase = False
            draw_btn.colour, erase_btn.colour = erase_btn.hover_colour, colour.BLUE_GREY
        if erase_btn.clicked():
            play_obj.erase = True
            erase_btn.colour, draw_btn.colour = erase_btn.hover_colour, colour.BLUE_GREY


@EventHandler.register(pygame.MOUSEBUTTONDOWN)
def clear_actions(play_obj: 'Play', event: pygame.event.Event) -> int:
    left_button = 1
    clear_options = play_obj.clear_options
    clear_options.menu_active = clear_options.rect.collidepoint(play_obj.pos)
    if event.button == left_button and clear_options.clicked():
        active_option = clear_options.active_option
        if clear_options.menu_active:
            clear_options.draw_menu = not clear_options.draw_menu
        elif clear_options.draw_menu and active_option >= 0:
            clear_options.draw_menu = False
            if active_option == 0:
                play_obj.clear_path()
            if active_option == 1:
                play_obj.clear_walls()
            if active_option == 2:
                play_obj.clear_grid()
            return active_option
    return clear_options.clicked()


@EventHandler.register(pygame.MOUSEBUTTONDOWN)
def speed_actions(play_obj: 'Play', event: pygame.event.Event) -> int:
    left_button = 1
    speed_btn = play_obj.speed_options.main
    speed_options = play_obj.speed_options
    speed_options.menu_active = speed_options.rect.collidepoint(play_obj.pos)
    if event.button == left_button and speed_options.clicked():
        active_option = speed_options.active_option
        if speed_options.menu_active:
            speed_options.draw_menu = not speed_options.draw_menu
        elif speed_options.draw_menu and active_option >= 0:
            speed_options.draw_menu = False
            speed_btn.text = speed_options.options[active_option]
            if active_option == 0:
                play_obj.speed = 25  # Slow
            if active_option == 1:
                play_obj.speed = 15  # Default
            if active_option == 2:
                play_obj.speed = 5  # Fast
            return active_option
    return speed_options.clicked()


@EventHandler.register(pygame.MOUSEBUTTONDOWN)
def visualize_state(play_obj: 'Play', event: pygame.event.Event) -> None:
    left_button = 1
    visualize_btn = play_obj.visualize_btn
    pathfinding_active_option = play_obj.pathfinding_options.active_option
    if event.button == left_button and visualize_btn.clicked():
        play_obj.pathfinding_options.draw_menu = False
        visualize_btn.colour = visualize_btn.hover_colour = colour.MAGENTA
        play_obj.pathfinding_hotkeys(pathfinding_active_option + PATHFINDING_KEY_OFFSET)
        if pathfinding_active_option + PATHFINDING_KEY_OFFSET in play_obj.pathfinding_keys:
            if not play_obj.start or not play_obj.end:
                play_obj.no_start_end_msg = True
    visualize_btn.colour, visualize_btn.hover_colour = colour.DARK_ORANGE, colour.ORANGE


@EventHandler.register(pygame.MOUSEBUTTONDOWN)
def pathfinding_actions(play_obj: 'Play', event: pygame.event.Event) -> None:
    pathfinding_btn = play_obj.pathfinding_options.main
    pathfinding_options = play_obj.pathfinding_options
    algo_actions(play_obj, event, pathfinding_btn, pathfinding_options)


def algo_actions(play_obj: 'Play', event: pygame.event.Event, algo_btn: 'Button', algo_options: 'DropDown') -> int:
    left_button = 1
    algo_options.menu_active = algo_options.rect.collidepoint(play_obj.pos)
    if event.button == left_button and algo_options.clicked():
        active_option = algo_options.active_option
        if algo_options.menu_active:
            algo_options.draw_menu = not algo_options.draw_menu
        elif algo_options.draw_menu and active_option >= 0:
            algo_options.draw_menu = False
            algo_btn.text = algo_options.options[active_option]
        return active_option
    return algo_options.clicked()


def hot_key_visualize(play_obj: 'Play', event: pygame.event.Event):
    visualize_btn = play_obj.visualize_btn
    pathfinding_btn = play_obj.pathfinding_options.main
    visualize_btn.colour = visualize_btn.hover_colour = colour.MAGENTA
    play_obj.clear_options.update()
    play_obj.speed_options.update()
    if event.key in play_obj.pathfinding_keys:
        play_obj.pathfinding_options.active_option = event.key - PATHFINDING_KEY_OFFSET
        pathfinding_btn.text = play_obj.pathfinding_options.options[event.key - PATHFINDING_KEY_OFFSET]
        if not play_obj.start or not play_obj.end:
            play_obj.no_start_end_msg = True
    play_obj.pathfinding_hotkeys(event.key)
    visualize_btn.colour, visualize_btn.hover_colour = colour.DARK_ORANGE, colour.ORANGE
