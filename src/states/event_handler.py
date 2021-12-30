import pygame
import colour
from typing import Callable, Dict, List, TYPE_CHECKING, Union

if TYPE_CHECKING:  # Avoid circular imports
    from .play import Play
    from ui.button import Button
    from ui.drop_down import DropDown

# Since pygame keys are integer constants
MAZE_KEY_OFFSET = 1073741883
PATHFINDING_KEY_OFFSET = 49


class EventHandler:
    """
    Handle input events using decorators to modify the behaviour of methods based on the event type and UI elements
    interacted

    Attributes:
        event_handler_registry: Dictionary of input events associated with its unique key and methods notified
    """
    event_handler_registry: Dict[Union[int, List[Callable[..., 'Play']]], List[Callable[..., pygame.event.Event]]] = {}

    @staticmethod
    def register(event_type: int) -> Callable[..., None]:
        """
        Store methods into event_handler_registry dictionary, registering them based on their event type

        Args:
            event_type: Integer constant of the event

        Returns:
            Decorator used to register an input events method
        """
        def decorator(func: Callable[..., pygame.event.Event]) -> None:
            EventHandler.event_handler_registry.setdefault(event_type, []).append(func)

        return decorator

    @staticmethod
    def notify(play_obj: 'Play', event: pygame.event.Event) -> None:
        """
        Subscribe methods to notifications based on their registered event type

        Args:
            play_obj: Game play state class instance
            event: Pygame object for representing events
        """
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
        if node.get_start():
            play_obj.drag_start = True
        elif node.get_end():
            play_obj.drag_end = True
        elif isinstance(node.get_bomb(), pygame.Surface):
            play_obj.drag_bomb = True
        if latest_click - play_obj.timer <= play_obj.double_click:
            play_obj.start_end_nodes(node)
        play_obj.timer = latest_click


@EventHandler.register(pygame.MOUSEMOTION)
def start_end_click_drag(play_obj: 'Play', *_) -> None:
    node = play_obj.node_pos()
    pathfinding_active_option = play_obj.pathfinding_options.active_option
    if play_obj.hold and node is not None and not node.get_wall() and not play_obj.erase:
        if play_obj.drag_start and play_obj.start is not None and node != play_obj.end:
            play_obj.start.reset()
            play_obj.start = node
            play_obj.start.set_start()
        elif play_obj.drag_end and play_obj.end is not None and node != play_obj.start:
            play_obj.end.reset()
            play_obj.end = node
            play_obj.end.set_end()
        if play_obj.path:
            play_obj.clear_open_nodes()
            if play_obj.auto_compute:
                play_obj.pathfinding_hotkeys(pathfinding_active_option + PATHFINDING_KEY_OFFSET)


@EventHandler.register(pygame.MOUSEMOTION)
def bomb_click_drag(play_obj: 'Play', *_) -> None:
    node = play_obj.node_pos()
    if play_obj.hold and node is not None and not node.get_wall() and not play_obj.erase:
        if play_obj.drag_bomb and play_obj.bomb and node != play_obj.start and node != play_obj.end:
            play_obj.bomb.reset()
            play_obj.bomb = node
            play_obj.bomb.set_bomb()


@EventHandler.register(pygame.MOUSEMOTION)
def click_drag(play_obj: 'Play', *_) -> None:
    node = play_obj.node_pos()
    pathfinding_active_option = play_obj.pathfinding_options.active_option
    if play_obj.hold and node is not None:
        if play_obj.erase:
            play_obj.clear_nodes(node)
        elif not play_obj.drag_start and not play_obj.drag_end and not play_obj.drag_bomb:
            play_obj.wall_nodes(node)
        if play_obj.path and play_obj.auto_compute:
            play_obj.clear_open_nodes()
            play_obj.pathfinding_hotkeys(pathfinding_active_option + PATHFINDING_KEY_OFFSET)


@EventHandler.register(pygame.MOUSEBUTTONUP)
def stop_click_drag(play_obj: 'Play', *_) -> None:
    play_obj.hold = False
    play_obj.auto_compute = False
    play_obj.drag_start = False
    play_obj.drag_end = False
    play_obj.drag_bomb = False


@EventHandler.register(pygame.MOUSEMOTION)
def dismiss_text(play_obj: 'Play', *_) -> None:
    if play_obj.no_path_msg:
        play_obj.no_path_msg = False
    if play_obj.no_start_end_msg:
        play_obj.no_start_end_msg = False


@EventHandler.register(pygame.KEYDOWN)
def hot_key_down(play_obj: 'Play', event: pygame.event.Event) -> None:
    play_obj.no_path_msg = False
    play_obj.maze_options.draw_menu = False
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
def bomb_state(play_obj: 'Play', event: pygame.event.Event) -> None:
    left_button = 1
    bomb_btn = play_obj.bomb_btn
    if event.button == left_button and bomb_btn.clicked():
        play_obj.hold = True
        if bomb_btn.text != play_obj.bomb_default_text and play_obj.bomb:
            play_obj.clear_nodes(play_obj.bomb)
            bomb_btn.text = play_obj.bomb_default_text
        else:
            play_obj.bomb_node()
            bomb_btn.text = "Remove 💣"


@EventHandler.register(pygame.MOUSEBUTTONDOWN)
def clear_actions(play_obj: 'Play', event: pygame.event.Event) -> None:
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


@EventHandler.register(pygame.MOUSEBUTTONDOWN)
def speed_actions(play_obj: 'Play', event: pygame.event.Event) -> None:
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
                play_obj.speed = 20  # Slow
            if active_option == 1:
                play_obj.speed = 10  # Default
            if active_option == 2:
                play_obj.speed = 0  # Fast


@EventHandler.register(pygame.MOUSEBUTTONDOWN)
def visualize_state(play_obj: 'Play', event: pygame.event.Event) -> None:
    left_button = 1
    visualize_btn = play_obj.visualize_btn
    maze_active_option = play_obj.maze_options.active_option
    pathfinding_active_option = play_obj.pathfinding_options.active_option
    if event.button == left_button and visualize_btn.clicked():
        play_obj.pathfinding_options.draw_menu = play_obj.maze_options.draw_menu = False
        visualize_btn.colour = visualize_btn.hover_colour = colour.MAGENTA
        play_obj.maze_hotkeys(maze_active_option + MAZE_KEY_OFFSET) if not play_obj.maze else \
            play_obj.pathfinding_hotkeys(pathfinding_active_option + PATHFINDING_KEY_OFFSET)
        if pathfinding_active_option + PATHFINDING_KEY_OFFSET in play_obj.pathfinding_keys:
            if not play_obj.start or not play_obj.end:
                play_obj.no_start_end_msg = True
    visualize_btn.colour, visualize_btn.hover_colour = colour.DARK_ORANGE, colour.ORANGE


@EventHandler.register(pygame.MOUSEBUTTONDOWN)
def maze_actions(play_obj: 'Play', event: pygame.event.Event) -> None:
    maze_btn = play_obj.maze_options.main
    maze_options = play_obj.maze_options
    algo_actions(play_obj, event, maze_btn, maze_options)


@EventHandler.register(pygame.MOUSEBUTTONDOWN)
def pathfinding_actions(play_obj: 'Play', event: pygame.event.Event) -> None:
    pathfinding_btn = play_obj.pathfinding_options.main
    pathfinding_options = play_obj.pathfinding_options
    algo_actions(play_obj, event, pathfinding_btn, pathfinding_options)


def algo_actions(play_obj: 'Play', event: pygame.event.Event, algo_btn: 'Button', algo_options: 'DropDown') -> None:
    left_button = 1
    algo_options.menu_active = algo_options.rect.collidepoint(play_obj.pos)
    if event.button == left_button and algo_options.clicked():
        active_option = algo_options.active_option
        if algo_options.menu_active:
            algo_options.draw_menu = not algo_options.draw_menu
        elif algo_options.draw_menu and active_option >= 0:
            algo_options.draw_menu = False
            algo_btn.text = algo_options.options[active_option]


def hot_key_visualize(play_obj: 'Play', event: pygame.event.Event) -> None:
    visualize_btn = play_obj.visualize_btn
    maze_btn = play_obj.maze_options.main
    pathfinding_btn = play_obj.pathfinding_options.main
    visualize_btn.colour = visualize_btn.hover_colour = colour.MAGENTA
    play_obj.clear_options.update()
    play_obj.speed_options.update()
    if event.key in play_obj.maze_keys:
        play_obj.maze_options.active_option = event.key - MAZE_KEY_OFFSET
        maze_btn.text = play_obj.maze_options.options[event.key - MAZE_KEY_OFFSET]
    if event.key in play_obj.pathfinding_keys:
        play_obj.pathfinding_options.active_option = event.key - PATHFINDING_KEY_OFFSET
        pathfinding_btn.text = play_obj.pathfinding_options.options[event.key - PATHFINDING_KEY_OFFSET]
        if not play_obj.start or not play_obj.end:
            play_obj.no_start_end_msg = True
    play_obj.maze_hotkeys(event.key)
    play_obj.pathfinding_hotkeys(event.key)
    visualize_btn.colour, visualize_btn.hover_colour = colour.DARK_ORANGE, colour.ORANGE
