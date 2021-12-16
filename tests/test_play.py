import pytest
import pygame
import random
from typing import Generator, Tuple
from pytest_mock import MockerFixture
from states.event_handler import EventHandler
from states.play import Play
from ui.node import Node


class TestPlay:

    # Act
    def test_divider(self, play_obj: Play) -> None:
        play_obj.divider()
        # Assert
        assert play_obj.nav_height == 3

    @pytest.mark.parametrize('pos', [(random.randint(0, 99999), random.randint(0, 99999)) for _ in range(5)])
    def test_node_pos(self, play_obj: Play, pos: Tuple[int, int], mocker: MockerFixture) -> None:
        mocker.patch('pygame.mouse.get_pos', return_value=pos)
        mocker.patch.object(Play, 'get_clicked_pos', return_value=(random.randint(play_obj.nav_height, play_obj.rows - 1),
                                                                   random.randint(play_obj.rect.top, play_obj.cols - 1)))
        node = play_obj.node_pos()
        assert isinstance(node, Node)

    @pytest.mark.parametrize('pos', [(random.randint(0, 99999), random.randint(0, 59)) for _ in range(5)])
    def test_fail_node_pos(self, play_obj: Play, pos: Tuple[int, int], mocker: MockerFixture) -> None:
        mocker.patch('pygame.mouse.get_pos', return_value=pos)
        assert play_obj.node_pos() is None

    def test_set_start_node(self, play_obj: Play, random_node: Generator[Node, None, None]) -> None:
        play_obj.start_end_nodes(next(random_node))
        if play_obj.start is not None:
            assert play_obj.start.set_start

    def test_set_end_node(self, play_obj: Play, random_node: Generator[Node, None, None]) -> None:
        play_obj.start = next(random_node)
        play_obj.start_end_nodes(next(random_node))
        if play_obj.end is not None:
            assert play_obj.end.set_end

    def test_wall_nodes(self, play_obj: Play, random_node: Generator[Node, None, None]) -> None:
        node = next(random_node)
        play_obj.wall_nodes(node)
        assert node.set_wall

    def test_bomb_node(self, play_obj: Play) -> None:
        play_obj.bomb_node()
        assert play_obj.bomb

    def test_random_bomb_node(self, play_obj: Play) -> None:
        play_obj.start = play_obj.grid[play_obj.rows // 2][play_obj.cols // 2]
        play_obj.bomb_node()
        assert play_obj.bomb

    def test_clear_start_node(self, play_obj: Play, random_node: Generator[Node, None, None]) -> None:
        play_obj.start = next(random_node)
        play_obj.clear_nodes(play_obj.start)
        assert play_obj.start is None

    def test_clear_end_node(self, play_obj: Play, random_node: Generator[Node, None, None]) -> None:
        play_obj.end = next(random_node)
        play_obj.clear_nodes(play_obj.end)
        assert play_obj.end is None

    def test_clear_bomb_node(self, play_obj: Play, random_node: Generator[Node, None, None]) -> None:
        play_obj.bomb = next(random_node)
        play_obj.clear_nodes(play_obj.bomb)
        assert play_obj.bomb_btn.text == play_obj.bomb_default_text
        assert play_obj.bomb is None

    def test_get_events(self, play_obj: Play, mocker: MockerFixture) -> None:
        mock_divider = mocker.patch.object(Play, 'divider')
        mock_draw_canvas = mocker.patch.object(Play, 'draw_canvas')
        mocker.patch('pygame.event.get', return_value=[pygame.USEREVENT])  # No play_obj events handled
        assert play_obj.run is True
        mocker.patch.object(EventHandler, 'notify', side_effect=lambda *args, **kwargs: setattr(play_obj, 'run', False))
        play_obj.get_events()
        assert play_obj.clock.get_fps() <= 60  # Compute clock's frame rate never runs more than 60fps
        mock_divider.assert_called()
        mock_draw_canvas.assert_called()
        assert play_obj.run is False

    def test_state_events(self, play_obj: Play, mocker: MockerFixture) -> None:
        mock_popup_helper = mocker.patch.object(Play, 'popup_helper', side_effect=lambda: setattr(play_obj, 'play',
                                                                                                  False))
        mocker.patch.object(Play, 'get_events')
        play_obj.clear_options.draw_menu = True  # Test dropdown menu is rendering its options
        play_obj.instructions = False
        play_obj.state_events()
        assert play_obj.draw_btn.colour == play_obj.draw_btn.hover_colour
        mock_popup_helper.assert_called()
        assert play_obj.play is False
