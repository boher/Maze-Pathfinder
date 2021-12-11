import pytest
import random
from typing import Generator, List
from pytest_mock import MockerFixture
from .test_canvas import TestCanvas
from .test_algos import TestAlgos
from algos.algos import Algos
from algos.dijkstras import Dijkstras
from ui.node import Node


class TestDijkstras(TestAlgos):

    # Arrange
    @pytest.fixture
    def dijkstras(self, algos: Algos, mocker: MockerFixture) -> Dijkstras:
        canvas_mock = mocker.Mock(spec=TestCanvas)
        return Dijkstras(canvas_mock.draw, algos.grid, algos.start, algos.end, algos.speed, algos.auto_compute)

    # Act
    def test_init(self, dijkstras: Dijkstras, grid: List[List[Node]]) -> None:
        # Assert
        assert dijkstras.distances == {node: float("inf") for row in grid for node in row}

    def test_put_open_set(self, dijkstras: Dijkstras, random_node: Generator[Node, None, None]) -> None:
        dijkstras.start = next(random_node)
        dijkstras.put_open_set()
        assert dijkstras.distances[dijkstras.start] == 0
        assert dijkstras.open_set.queue == [(0, dijkstras.start)]

    def test_compare_neighbours(self, dijkstras: Dijkstras, random_node: Generator[Node, None, None],
                                mocker: MockerFixture) -> None:
        mocker.patch.object(Dijkstras, 'set_speed')
        mocker.patch.object(Node, 'get_wall', return_value=False)
        current = next(random_node)
        dijkstras.distances[current] = 0
        current.neighbours = [random.choice(list(dijkstras.distances.keys())),
                              random.choice(list(dijkstras.distances.keys())),
                              random.choice(list(dijkstras.distances.keys())),
                              random.choice(list(dijkstras.distances.keys()))]
        dijkstras.compare_neighbours(current)
        for neighbour in current.neighbours:
            assert neighbour.get_wall
            assert dijkstras.came_from[neighbour] == current
            assert dijkstras.curr_distance > 1

    def test_execute(self, dijkstras: Dijkstras, random_node: Generator[Node, None, None],
                     mocker: MockerFixture) -> None:
        dijkstras.start = dijkstras.end = next(random_node)
        canvas_mock = mocker.Mock(spec=TestCanvas)
        mock_completed_path = mocker.patch.object(Dijkstras, 'completed_path')
        result = dijkstras.execute()
        assert dijkstras.open_set.not_empty
        mock_completed_path.assert_called()
        assert canvas_mock.draw
        assert result is True

    def test_execute_no_path(self, dijkstras: Dijkstras, random_node: Generator[Node, None, None],
                             mocker: MockerFixture) -> None:
        dijkstras.start = current = next(random_node)
        canvas_mock = mocker.Mock(spec=TestCanvas)
        result = dijkstras.execute()
        assert dijkstras.curr_distance > dijkstras.distances[current]
        assert dijkstras.open_set.empty()
        assert canvas_mock.draw
        assert result is False
