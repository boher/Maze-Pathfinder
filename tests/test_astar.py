import pytest
import random
from typing import Generator
from pytest_mock import MockerFixture
from .test_canvas import TestCanvas
from .test_algos import TestAlgos
from algos.a_star import AStar
from algos.algos import Algos
from ui.node import Node


class TestAStar(TestAlgos):

    # Arrange
    @pytest.fixture
    def astar(self, algos: Algos, mocker: MockerFixture) -> AStar:
        canvas_mock = mocker.Mock(spec=TestCanvas)
        return AStar(canvas_mock.draw, algos.grid, algos.start, algos.end, algos.speed, algos.auto_compute)

    # Act
    def test_init(self, astar: AStar) -> None:
        # Assert
        assert astar.count == 0
        assert astar.f_score == astar.g_score

    def test_put_open_set(self, astar: AStar, random_node: Generator[Node, None, None]) -> None:
        astar.start = next(random_node)
        astar.end = next(random_node)
        astar.put_open_set()
        assert astar.f_score[astar.start] == astar.manhattan_dist(astar.start.get_pos(), astar.end.get_pos())
        assert astar.g_score[astar.start] == 0
        assert astar.open_set.queue == [(0, 0, astar.start)]

    def test_compare_neighbours(self, astar: AStar, random_node: Generator[Node, None, None], mocker: MockerFixture) -> None:
        mocker.patch.object(AStar, 'set_speed')
        mocker.patch.object(AStar, 'manhattan_dist', return_value=12)
        astar.open_set_hash = {next(random_node)}
        current = next(random_node)
        astar.g_score[current] = 0
        current.neighbours = [random.choice(list(astar.g_score.keys())), random.choice(list(astar.g_score.keys())),
                              random.choice(list(astar.g_score.keys())), random.choice(list(astar.g_score.keys()))]
        astar.compare_neighbours(current)  # RMB temp_g_score is g_score[current] + 1, basically just 1 and increments
        for neighbour in current.neighbours:
            assert astar.came_from[neighbour] == current
            assert astar.g_score[neighbour] == 1
            assert astar.f_score[neighbour] == 12 + 1
            assert neighbour != astar.end
            assert not neighbour.get_start()
            assert not neighbour.get_end()
            assert neighbour.get_open()
        assert astar.count == len(astar.open_set_hash) - 1
        assert astar.open_set.qsize() == len(astar.open_set_hash) - 1

    def test_compare_neighbours_wall(self, astar: AStar, random_node: Generator[Node, None, None]) -> None:
        current = next(random_node)
        neighbour_wall = random.choice(list(astar.g_score.keys()))
        neighbour_wall.set_wall()
        current.neighbours = [neighbour_wall]
        astar.compare_neighbours(current)
        assert current.neighbours.pop().get_wall()
        assert not neighbour_wall.get_open()

    def test_execute(self, astar: AStar, random_node: Generator[Node, None, None], mocker: MockerFixture) -> None:
        astar.start = astar.end = next(random_node)
        canvas_mock = mocker.Mock(spec=TestCanvas)
        mock_completed_path = mocker.patch.object(AStar, 'completed_path')
        result = astar.execute()
        assert astar.open_set.not_empty
        mock_completed_path.assert_called()
        assert canvas_mock.draw
        assert result is True

    def test_execute_no_path(self, astar: AStar, random_node: Generator[Node, None, None],
                             mocker: MockerFixture) -> None:
        astar.start = next(random_node)
        canvas_mock = mocker.Mock(spec=TestCanvas)
        result = astar.execute()
        assert not astar.open_set_hash
        assert astar.open_set.empty()
        assert canvas_mock.draw
        assert result is False
