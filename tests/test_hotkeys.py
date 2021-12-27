import pygame
from typing import Generator
from pytest_mock import MockerFixture
from states.play import Play
from algos.a_star import AStar
from ui.node import Node


class TestHotKeys:

    # Act
    def test_update_no_path(self, play_obj: Play) -> None:
        play_obj.no_path_msg = True
        play_obj.update()
        # Assert
        assert play_obj.render

    def test_update_no_start_end(self, play_obj: Play) -> None:
        play_obj.no_start_end_msg = True
        play_obj.update()
        assert play_obj.render

    def test_pathfinding_hotkeys(self, play_obj: Play, random_node: Generator[Node, None, None], mocker: MockerFixture) -> None:
        play_obj.start = next(random_node)
        play_obj.end = next(random_node)
        mocker.patch.object(AStar, 'execute', return_value=False)
        play_obj.pathfinding_hotkeys(pygame.K_2)
        assert play_obj.pathfinding_options.clicked
        assert play_obj.clear_path
        assert play_obj.node_traversal
        assert play_obj.path is False
        assert play_obj.no_path_msg is True

    def test_pathfind_bomb(self, play_obj: Play, random_node: Generator[Node, None, None], mocker: MockerFixture) -> None:
        play_obj.start = next(random_node)
        play_obj.end = next(random_node)
        play_obj.bomb = next(random_node)
        mocker.patch.object(AStar, 'execute', return_value=True)
        play_obj.pathfinding_hotkeys(pygame.K_2)
        assert play_obj.pathfinding_options.clicked
        assert play_obj.clear_path
        assert play_obj.node_traversal
        assert play_obj.start.visited is False
        assert play_obj.path is True

    def test_clear_open_nodes(self, play_obj: Play) -> None:
        play_obj.clear_open_nodes()
        assert play_obj.auto_compute is True
        assert play_obj.reset_open_nodes

    def test_clearing_keys_z(self, play_obj: Play, mocker: MockerFixture) -> None:
        mock_clear_path = mocker.patch.object(Play, 'clear_path')
        play_obj.clearing_keys(pygame.K_z)
        mock_clear_path.assert_called()

    def test_clearing_keys_x(self, play_obj: Play, mocker: MockerFixture) -> None:
        mock_clear_walls = mocker.patch.object(Play, 'clear_walls')
        play_obj.clearing_keys(pygame.K_x)
        mock_clear_walls.assert_called()

    def test_clearing_keys_c(self, play_obj: Play, mocker: MockerFixture) -> None:
        mock_clear_grid = mocker.patch.object(Play, 'clear_grid')
        play_obj.clearing_keys(pygame.K_c)
        mock_clear_grid.assert_called()

    def test_clear_path(self, play_obj: Play, random_node: Generator[Node, None, None]) -> None:
        play_obj.start = next(random_node)
        play_obj.end = next(random_node)
        play_obj.path = True
        play_obj.clear_path()
        assert play_obj.path is False
        assert play_obj.reset_traversed_path

    def test_clear_walls(self, play_obj: Play) -> None:
        play_obj.clear_walls()
        assert play_obj.reset_walls

    def test_clear_grid(self, play_obj: Play, mocker: MockerFixture) -> None:
        play_obj.bomb_btn = mocker.Mock()
        mock_create_grid = mocker.patch.object(Play, 'create_grid')
        play_obj.clear_grid()
        mock_create_grid.assert_called()
        assert play_obj.bomb_btn.text == play_obj.bomb_default_text
        assert play_obj.start is None
        assert play_obj.end is None
        assert play_obj.bomb is None
        assert play_obj.path is False
