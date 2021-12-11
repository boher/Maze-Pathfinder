import pytest
import pygame
from typing import Callable, Dict, Generator, List, Tuple, cast
from pytest_mock import MockerFixture
from .test_canvas import TestCanvas
from algos.algos import Algos
from ui.node import Node


class TestAlgos:

    # Arrange
    @pytest.fixture
    def algos(self, grid: List[List[Node]], random_node: Generator[Node, None, None]) -> Algos:
        start = next(random_node)
        end = next(random_node)
        draw = cast(Callable[[], None], TestCanvas.draw)
        return Algos(draw=draw, grid=grid, start=start, end=end, speed=15, auto_compute=False)

    @pytest.fixture(autouse=True)
    def init_test_nodes(self, random_node: Generator[Node, None, None]):
        self.test_node_1 = next(random_node)
        self.test_node_2 = next(random_node)
        self.test_node_3 = next(random_node)
        self.test_node_4 = next(random_node)
        self.test_node_5 = next(random_node)
        self.test_node_6 = next(random_node)
        self.test_node_7 = next(random_node)
        self.test_node_8 = next(random_node)

    # Act
    def test_speed(self, algos: Algos) -> None:
        # Assert
        assert algos.speed % 5 == 0

    @pytest.mark.parametrize('p1, p2, expected',
                             [((0, 0), (0, 0), 0), ((200, 200), (200, 200), 0), ((400, 400), (400, 400), 0),
                              ((600, 600), (600, 600), 0), ((800, 800), (800, 800), 0),
                              ((1000, 1000), (1000, 1000), 0)])
    def test_manhattan_dist(self, algos: Algos, p1: Tuple[int, int], p2: Tuple[int, int], expected: int) -> None:
        assert algos.manhattan_dist(p1, p2) is expected

    def test_optimal_path(self, algos: Algos, mocker: MockerFixture) -> None:
        canvas_mock = mocker.Mock(spec=TestCanvas)
        came_from, current = self.get_mock_came_from_current()
        algos.optimal_path(came_from, current, canvas_mock.draw)
        assert current in came_from
        assert current.set_path
        if not algos.auto_compute:
            assert algos.set_speed
            assert canvas_mock.draw

    def test_append_bomb_path(self, algos: Algos) -> None:
        came_from, current = self.get_mock_came_from_current()
        algos.append_bomb_path(came_from, current)
        assert algos.bomb_path

    def test_optimal_bomb_path(self, algos: Algos, mocker: MockerFixture) -> None:
        canvas_mock = mocker.Mock(spec=TestCanvas)
        full_path_mock = []
        for num in range(1, 9):
            test_node = getattr(self, f"test_node_{num}")
            full_path_mock.append(test_node)
        mocker.patch.object(Algos, 'is_bomb', return_value=False)
        algos.optimal_bomb_path(canvas_mock.draw, full_path_mock)
        for current in full_path_mock:
            assert current.set_path
        if not algos.auto_compute:
            assert algos.set_speed
            assert canvas_mock.draw

    def test_completed_path_with_bomb(self, algos: Algos, random_node: Generator[Node, None, None],
                                      mocker: MockerFixture) -> None:
        start = next(random_node)
        end = next(random_node)
        canvas_mock = mocker.Mock(spec=TestCanvas)
        came_from, current = self.get_mock_came_from_current()
        mocker.patch.object(Algos, 'is_bomb', return_value=True)
        mocker.patch.object(Algos, 'append_bomb_path')
        algos.completed_path(came_from, start, end, canvas_mock.draw)
        assert algos.is_bomb(algos.start)
        assert algos.is_bomb(algos.end)

    def test_completed_path_no_bomb(self, algos: Algos, random_node: Generator[Node, None, None],
                                    mocker: MockerFixture) -> None:
        start = next(random_node)
        end = next(random_node)
        canvas_mock = mocker.Mock(spec=TestCanvas)
        came_from, current = self.get_mock_came_from_current()
        mocker.patch.object(Algos, 'is_bomb', return_value=False)
        mocker.patch.object(Algos, 'optimal_path')
        algos.completed_path(came_from, start, end, canvas_mock.draw)
        assert start.get_start()
        assert not algos.bomb_path

    def test_is_bomb(self, algos: Algos, random_node: Generator[Node, None, None]) -> None:
        node = next(random_node)
        node.set_bomb()
        algos.is_bomb(node)
        assert isinstance(node.colour, pygame.Surface)

    def test_not_bomb(self, algos: Algos, random_node: Generator[Node, None, None]) -> None:
        node = next(random_node)
        algos.is_bomb(node)
        assert not isinstance(node.colour, pygame.Surface)

    def test_put_closed_set_with_bomb(self, algos: Algos, mocker: MockerFixture) -> None:
        _, current = self.get_mock_came_from_current()
        current.set_bomb()
        mocker.patch.object(Algos, 'is_bomb', return_value=True)
        algos.put_closed_set(current)
        assert current.set_bomb_closed

    def test_put_closed_set_no_bomb(self, algos: Algos, mocker: MockerFixture) -> None:
        _, current = self.get_mock_came_from_current()
        current.set_open()
        mocker.patch.object(Algos, 'is_bomb', return_value=False)
        algos.put_closed_set(current)
        assert current.set_closed

    def test_no_path(self, algos: Algos) -> None:
        assert algos.no_path()

    def test_safe_quit(self, algos: Algos, mocker: MockerFixture) -> None:
        mock_pygame_quit = mocker.patch('pygame.quit')
        pygame.event.post(pygame.event.Event(pygame.QUIT))
        with pytest.raises(SystemExit):
            algos.safe_quit()
            mock_pygame_quit.assert_called_once()

    def get_mock_came_from_current(self) -> Tuple[Dict[Node, Node], Node]:
        came_from = {
            self.test_node_1: self.test_node_2,
            self.test_node_8: self.test_node_3,
            self.test_node_7: self.test_node_4,
            self.test_node_6: self.test_node_5,
            self.test_node_5: self.test_node_1
        }
        current = self.test_node_8
        return came_from, current
