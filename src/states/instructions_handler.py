import pygame
import webbrowser
from typing import Callable, Dict, List, TYPE_CHECKING, Union

if TYPE_CHECKING:  # Avoid circular imports
    from .instructions import Instructions


class InstructionsHandler:
    """
    Handle instructions events using decorators to modify the behaviour of methods based on the event type and UI
    elements interacted

    Attributes:
        instructions_registry: Dictionary of instructions events associated with its unique key and methods notified
    """
    instructions_registry: Dict[
        Union[int, List[Callable[..., 'Instructions']]], List[Callable[..., pygame.event.Event]]] = {}

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
            InstructionsHandler.instructions_registry.setdefault(event_type, []).append(func)

        return decorator

    @staticmethod
    def notify(instructions: 'Instructions', event: pygame.event.Event) -> None:
        """
        Subscribe methods to notifications based on their registered event type

        Args:
            instructions: Instructions class instance
            event: Pygame object for representing events
        """
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
            while instructions.index < 3:
                instructions.index += 1
                break
        if back_btn.clicked():
            while instructions.index > 0:
                instructions.index -= 1
                break


@InstructionsHandler.register(pygame.MOUSEBUTTONDOWN)
def learn_more_pathfinding_actions(instructions: 'Instructions', event: pygame.event.Event) -> None:
    left_button = 1
    pathfinding_active_option = instructions.pathfinding_options.active_option
    visualgo_resource = instructions.visualgo_resource
    if event.button == left_button and visualgo_resource.clicked():
        if instructions.path:
            if pathfinding_active_option < 2:
                webbrowser.open(f"https://visualgo.net/en/sssp?slide={pathfinding_active_option + 7}")
            if pathfinding_active_option == 2:
                webbrowser.open(f"https://visualgo.net/en/bst?slide={pathfinding_active_option - 1}")
            if pathfinding_active_option > 2:
                webbrowser.open(f"https://visualgo.net/en/sssp?slide={pathfinding_active_option * 3 - 3}")


@InstructionsHandler.register(pygame.MOUSEBUTTONDOWN)
def learn_more_actions(instructions: 'Instructions', event: pygame.event.Event) -> None:
    left_button = 1
    handson_resource = instructions.handson_resource
    github_repo = instructions.github_repo
    if event.button == left_button:
        if handson_resource.clicked():
            if instructions.maze_options.active_option > -1 and not instructions.path:
                webbrowser.open("https://www.jamisbuck.org/mazes")
            if instructions.pathfinding_options.active_option > -1 and instructions.path:
                webbrowser.open("https://www.redblobgames.com/pathfinding")
        if github_repo.clicked():
            webbrowser.open("https://github.com/boher/Maze-Pathfinder")
