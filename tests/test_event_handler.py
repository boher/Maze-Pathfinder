import pytest
import pygame
from typing import Generator
from pytest_mock import MockerFixture
from states.event_handler import EventHandler
from states.event_handler import MAZE_KEY_OFFSET, PATHFINDING_KEY_OFFSET
from states.play import Play
from ui.node import Node


class TestEventHandler:

    # Arrange
    @pytest.fixture
    def event_handler(self) -> EventHandler:
        return EventHandler()

    # Act
    def test_event_handler_register(self, event_handler: EventHandler) -> None:
        decorator = event_handler.register(pygame.MOUSEMOTION)
        # Assert
        assert all(key in event_handler.event_handler_registry.keys() for key in (pygame.QUIT, pygame.MOUSEBUTTONDOWN,
                                                                                  pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP,
                                                                                  pygame.KEYDOWN))
        assert decorator.__name__ == "decorator"

    def test_safe_quit(self, play_obj: Play, mocker: MockerFixture) -> None:
        mock_pygame_quit = mocker.patch('pygame.quit')
        with pytest.raises(SystemExit):
            quit_event = pygame.event.Event(pygame.QUIT)
            EventHandler.notify(play_obj, quit_event)
            assert play_obj.run is False
            assert play_obj.play is False
            mock_pygame_quit.assert_called_once()

    def test_helper_state(self, play_obj: Play, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch.object(play_obj.helper_btn, 'clicked', return_value=True)
        mock_popup_helper = mocker.patch.object(Play, 'popup_helper')
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.hold is True
        assert play_obj.instructions
        mock_popup_helper.assert_called()

    def test_start_double_left_click(self, play_obj: Play, random_node: Generator[Node, None, None],
                                     mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        play_obj.start = next(random_node)
        play_obj.start.set_start()
        mocker.patch.object(Play, 'node_pos', return_value=play_obj.start)
        mock_start_end_nodes = mocker.patch.object(Play, 'start_end_nodes')
        play_obj.timer = 99999
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.drag_start is True
        assert play_obj.drag_end is False
        assert play_obj.drag_bomb is False
        mock_start_end_nodes.assert_called_with(play_obj.start)

    def test_end_double_left_click(self, play_obj: Play, random_node: Generator[Node, None, None],
                                   mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        play_obj.end = next(random_node)
        play_obj.end.set_end()
        mocker.patch.object(Play, 'node_pos', return_value=play_obj.end)
        mock_start_end_nodes = mocker.patch.object(Play, 'start_end_nodes')
        play_obj.timer = 99999
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.drag_end is True
        assert play_obj.drag_start is False
        assert play_obj.drag_bomb is False
        mock_start_end_nodes.assert_called_with(play_obj.end)

    def test_bomb_double_left_click(self, play_obj: Play, random_node: Generator[Node, None, None],
                                    mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        play_obj.bomb = next(random_node)
        play_obj.bomb.set_bomb()
        mocker.patch.object(Play, 'node_pos', return_value=play_obj.bomb)
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.drag_bomb is True
        assert play_obj.drag_end is False
        assert play_obj.drag_start is False

    def test_start_click_drag(self, play_obj: Play, random_node: Generator[Node, None, None], mocker: MockerFixture) -> None:
        mouse_motion_event = pygame.event.Event(pygame.MOUSEMOTION)
        play_obj.start = next(random_node)
        mocker.patch.object(Play, 'node_pos', return_value=play_obj.start)
        mock_start_reset = mocker.patch.object(play_obj.start, 'reset')
        mock_pathfinding_hotkeys = mocker.patch.object(Play, 'pathfinding_hotkeys')
        play_obj.hold = True
        play_obj.drag_start = True
        play_obj.path = True
        EventHandler.notify(play_obj, mouse_motion_event)
        assert play_obj.erase is False
        mock_start_reset.assert_called()
        assert play_obj.auto_compute is True
        mock_pathfinding_hotkeys.assert_called_with(play_obj.pathfinding_options.active_option + PATHFINDING_KEY_OFFSET)

    def test_end_click_drag(self, play_obj: Play, random_node: Generator[Node, None, None], mocker: MockerFixture) -> None:
        mouse_motion_event = pygame.event.Event(pygame.MOUSEMOTION)
        play_obj.end = next(random_node)
        mocker.patch.object(Play, 'node_pos', return_value=play_obj.end)
        mock_end_reset = mocker.patch.object(play_obj.end, 'reset')
        play_obj.hold = True
        play_obj.drag_end = True
        EventHandler.notify(play_obj, mouse_motion_event)
        assert play_obj.erase is False
        mock_end_reset.assert_called()

    def test_bomb_click_drag(self, play_obj: Play, random_node: Generator[Node, None, None],
                             mocker: MockerFixture) -> None:
        mouse_motion_event = pygame.event.Event(pygame.MOUSEMOTION)
        play_obj.bomb = next(random_node)
        mocker.patch.object(Play, 'node_pos', return_value=play_obj.bomb)
        mock_bomb_reset = mocker.patch.object(play_obj.bomb, 'reset')
        play_obj.hold = True
        play_obj.drag_bomb = True
        EventHandler.notify(play_obj, mouse_motion_event)
        assert play_obj.erase is False
        mock_bomb_reset.assert_called()

    def test_erase_click_drag(self, play_obj: Play, random_node: Generator[Node, None, None], mocker: MockerFixture) -> None:
        mouse_motion_event = pygame.event.Event(pygame.MOUSEMOTION)
        node = next(random_node)
        mocker.patch.object(Play, 'node_pos', return_value=node)
        mock_clear_nodes = mocker.patch.object(Play, 'clear_nodes')
        play_obj.hold = True
        play_obj.erase = True
        EventHandler.notify(play_obj, mouse_motion_event)
        mock_clear_nodes.assert_called_with(node)

    def test_wall_click_drag(self, play_obj: Play, random_node: Generator[Node, None, None], mocker: MockerFixture) -> None:
        mouse_motion_event = pygame.event.Event(pygame.MOUSEMOTION)
        node = next(random_node)
        mocker.patch.object(Play, 'node_pos', return_value=node)
        mock_wall_nodes = mocker.patch.object(Play, 'wall_nodes')
        play_obj.hold = True
        EventHandler.notify(play_obj, mouse_motion_event)
        assert play_obj.drag_start is False
        assert play_obj.drag_end is False
        assert play_obj.drag_bomb is False
        mock_wall_nodes.assert_called_with(node)

    def test_autocompute_click_drag(self, play_obj: Play, random_node: Generator[Node, None, None], mocker: MockerFixture) -> None:
        mouse_motion_event = pygame.event.Event(pygame.MOUSEMOTION)
        mocker.patch.object(Play, 'node_pos', return_value=next(random_node))
        mock_pathfinding_hotkeys = mocker.patch.object(Play, 'pathfinding_hotkeys')
        play_obj.hold = True
        play_obj.path = True
        play_obj.auto_compute = True
        EventHandler.notify(play_obj, mouse_motion_event)
        mock_pathfinding_hotkeys.assert_called_with(play_obj.pathfinding_options.active_option + PATHFINDING_KEY_OFFSET)

    def test_stop_click_drag(self, play_obj: Play) -> None:
        mouse_up_event = pygame.event.Event(pygame.MOUSEBUTTONUP)
        EventHandler.notify(play_obj, mouse_up_event)
        assert play_obj.hold is False
        assert play_obj.auto_compute is False
        assert play_obj.drag_start is False
        assert play_obj.drag_end is False
        assert play_obj.drag_bomb is False

    def test_dismiss_no_path(self, play_obj: Play) -> None:
        mouse_motion_event = pygame.event.Event(pygame.MOUSEMOTION)
        play_obj.no_path_msg = True
        EventHandler.notify(play_obj, mouse_motion_event)
        assert play_obj.no_path_msg is False

    def test_dismiss_no_start_end(self, play_obj: Play) -> None:
        mouse_motion_event = pygame.event.Event(pygame.MOUSEMOTION)
        play_obj.no_start_end_msg = True
        EventHandler.notify(play_obj, mouse_motion_event)
        assert play_obj.no_start_end_msg is False

    def test_helper_key_down(self, play_obj: Play, mocker: MockerFixture) -> None:
        key_down_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_h)
        mock_popup_helper = mocker.patch.object(Play, 'popup_helper')
        EventHandler.notify(play_obj, key_down_event)
        assert play_obj.instructions is True
        mock_popup_helper.assert_called()

    def test_maze_key_down(self, play_obj: Play, mocker: MockerFixture) -> None:
        key_down_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_F2)
        mock_maze_hotkeys = mocker.patch.object(Play, 'maze_hotkeys')
        maze_btn = play_obj.maze_options.main
        EventHandler.notify(play_obj, key_down_event)
        assert key_down_event.key in play_obj.maze_keys
        assert play_obj.maze_options.options[play_obj.maze_options.active_option] == maze_btn.text
        mock_maze_hotkeys.assert_called_with(key_down_event.key)

    def test_pathfinding_key_down(self, play_obj: Play, mocker: MockerFixture) -> None:
        key_down_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_2)
        mock_pathfinding_hotkeys = mocker.patch.object(Play, 'pathfinding_hotkeys')
        pathfinding_btn = play_obj.pathfinding_options.main
        EventHandler.notify(play_obj, key_down_event)
        assert key_down_event.key in play_obj.pathfinding_keys
        assert play_obj.pathfinding_options.options[play_obj.pathfinding_options.active_option] == pathfinding_btn.text
        mock_pathfinding_hotkeys.assert_called_with(key_down_event.key)

    def test_clearing_key_down(self, play_obj: Play, mocker: MockerFixture) -> None:
        key_down_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c)
        mock_clearing_keys = mocker.patch.object(Play, 'clearing_keys')
        EventHandler.notify(play_obj, key_down_event)
        mock_clearing_keys.assert_called_with(key_down_event.key)

    def test_draw_state(self, play_obj: Play, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch.object(play_obj.draw_btn, 'clicked', return_value=True)
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.hold is True
        assert play_obj.erase is False
        assert play_obj.draw_btn.colour == play_obj.erase_btn.hover_colour

    def test_erase_state(self, play_obj: Play, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch.object(play_obj.erase_btn, 'clicked', return_value=True)
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.hold is True
        assert play_obj.erase is True
        assert play_obj.erase_btn.colour == play_obj.erase_btn.hover_colour

    def test_add_bomb_state(self, play_obj: Play, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch.object(play_obj.bomb_btn, 'clicked', return_value=True)
        mock_add_bomb = mocker.patch.object(Play, 'bomb_node')
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.hold is True
        mock_add_bomb.assert_called()
        assert "Remove" in play_obj.bomb_btn.text

    def test_remove_bomb_state(self, play_obj: Play, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch.object(play_obj.bomb_btn, 'clicked', return_value=True)
        mock_clear_bomb = mocker.patch.object(Play, 'clear_nodes')
        # Mock bomb has been added
        play_obj.bomb_node()
        play_obj.bomb_btn.text = "Remove 💣"
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.hold is True
        mock_clear_bomb.assert_called_with(play_obj.bomb)
        assert play_obj.bomb_btn.text == play_obj.bomb_default_text

    def test_clear_path_actions(self, play_obj: Play, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        play_obj.clear_options.active_option = 0
        mock_clear_path = mocker.patch.object(Play, 'clear_path')
        play_obj.clear_options.main.pos = play_obj.clear_options.rect.center
        play_obj.clear_options.draw_menu = True
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.clear_options.draw_menu is False
        mock_clear_path.assert_called()

    def test_clear_walls_actions(self, play_obj: Play, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        play_obj.clear_options.active_option = 1
        mock_clear_walls = mocker.patch.object(Play, 'clear_walls')
        play_obj.clear_options.main.pos = play_obj.clear_options.rect.center
        play_obj.clear_options.draw_menu = True
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.clear_options.draw_menu is False
        mock_clear_walls.assert_called()

    def test_clear_grid_actions(self, play_obj: Play, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        play_obj.clear_options.active_option = 2
        mock_clear_grid = mocker.patch.object(Play, 'clear_grid')
        play_obj.clear_options.main.pos = play_obj.clear_options.rect.center
        play_obj.clear_options.draw_menu = True
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.clear_options.draw_menu is False
        mock_clear_grid.assert_called()

    def test_slow_speed_actions(self, play_obj: Play) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        active_option = play_obj.speed_options.active_option = 0
        speed_btn = play_obj.speed_options.main
        speed_btn.pos = play_obj.speed_options.rect.center
        play_obj.speed_options.draw_menu = True
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.speed_options.draw_menu is False
        assert play_obj.speed_options.options[active_option] == speed_btn.text
        assert play_obj.speed == 20

    def test_default_speed_actions(self, play_obj: Play) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        active_option = play_obj.speed_options.active_option = 1
        speed_btn = play_obj.speed_options.main
        speed_btn.pos = play_obj.speed_options.rect.center
        play_obj.speed_options.draw_menu = True
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.speed_options.draw_menu is False
        assert play_obj.speed_options.options[active_option] == speed_btn.text
        assert play_obj.speed == 10

    def test_fast_speed_actions(self, play_obj: Play) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        active_option = play_obj.speed_options.active_option = 2
        speed_btn = play_obj.speed_options.main
        speed_btn.pos = play_obj.speed_options.rect.center
        play_obj.speed_options.draw_menu = True
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.speed_options.draw_menu is False
        assert play_obj.speed_options.options[active_option] == speed_btn.text
        assert play_obj.speed == 0

    def test_visualize_maze_state(self, play_obj: Play, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch.object(play_obj.visualize_btn, 'clicked', return_value=True)
        mock_maze_hotkeys = mocker.patch.object(Play, 'maze_hotkeys')
        play_obj.maze_options.active_option = 0
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        mock_maze_hotkeys.assert_called_with(play_obj.maze_options.active_option + MAZE_KEY_OFFSET)

    def test_visualize_pathfinding_state(self, play_obj: Play, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch.object(play_obj.visualize_btn, 'clicked', return_value=True)
        mock_pathfinding_hotkeys = mocker.patch.object(Play, 'pathfinding_hotkeys')
        play_obj.pathfinding_options.active_option = 3
        play_obj.maze = True
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.start is None
        assert play_obj.end is None
        assert play_obj.no_start_end_msg is True
        mock_pathfinding_hotkeys.assert_called_with(play_obj.pathfinding_options.active_option + PATHFINDING_KEY_OFFSET)

    def test_maze_actions(self, play_obj: Play) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        active_option = play_obj.maze_options.active_option = 0
        maze_btn = play_obj.maze_options.main
        maze_btn.pos = play_obj.maze_options.rect.center
        play_obj.maze_options.draw_menu = True
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert not play_obj.maze_options.draw_menu
        assert play_obj.maze_options.options[active_option] == maze_btn.text

    def test_pathfinding_actions(self, play_obj: Play) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        active_option = play_obj.pathfinding_options.active_option = 2
        pathfinding_btn = play_obj.pathfinding_options.main
        pathfinding_btn.pos = play_obj.pathfinding_options.rect.center
        play_obj.pathfinding_options.draw_menu = True
        EventHandler.notify(play_obj, mouse_down_event)
        assert mouse_down_event.button == 1
        assert play_obj.pathfinding_options.draw_menu is False
        assert play_obj.pathfinding_options.options[active_option] == pathfinding_btn.text
