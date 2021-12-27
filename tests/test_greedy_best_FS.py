import pytest
from typing import Generator
from pytest_mock import MockerFixture
from .test_canvas import TestCanvas
from .test_algos import TestAlgos
from algos.algos import Algos
from algos.greedy_best_fs import GreedyBestFS
from ui.node import Node


class TestGreedyBestFS(TestAlgos):

    # Arrange
    @pytest.fixture
    def greedy_best_fs(self, algos: Algos, mocker: MockerFixture) -> GreedyBestFS:
        canvas_mock = mocker.Mock(spec=TestCanvas)
        return GreedyBestFS(canvas_mock.draw, algos.grid, algos.start, algos.end, algos.speed, algos.auto_compute)

    # Act
    def test_put_open_set(self, greedy_best_fs: GreedyBestFS, random_node: Generator[Node, None, None]) -> None:
        greedy_best_fs.start = next(random_node)
        greedy_best_fs.end = next(random_node)
        greedy_best_fs.put_open_set()
        # Assert
        assert greedy_best_fs.open_set.queue == [(greedy_best_fs.manhattan_dist(
            greedy_best_fs.start.get_pos(), greedy_best_fs.end.get_pos()), greedy_best_fs.start)]

    def test_compare_neighbours(self, greedy_best_fs: GreedyBestFS, random_node: Generator[Node, None, None],
                                mocker: MockerFixture) -> None:
        mocker.patch.object(GreedyBestFS, 'set_speed')
        mocker.patch.object(GreedyBestFS, 'manhattan_dist', return_value=12)
        current = next(random_node)
        current.neighbours = [next(random_node), next(random_node), next(random_node), next(random_node)]
        greedy_best_fs.compare_neighbours(current)
        for neighbour in current.neighbours:
            assert greedy_best_fs.came_from[neighbour] == current
            assert neighbour.visited
            assert neighbour != greedy_best_fs.end
            assert not neighbour.get_start()
            assert not neighbour.get_end()
            assert neighbour.get_open()

    def test_compare_neighbours_wall(self, greedy_best_fs: GreedyBestFS, random_node: Generator[Node, None, None]) -> None:
        current = next(random_node)
        neighbour_wall = next(random_node)
        neighbour_wall.set_wall()
        current.neighbours = [neighbour_wall]
        greedy_best_fs.compare_neighbours(current)
        assert current.neighbours.pop().get_wall()
        assert not neighbour_wall.get_open()

    def test_execute(self, greedy_best_fs: GreedyBestFS, random_node: Generator[Node, None, None],
                     mocker: MockerFixture) -> None:
        greedy_best_fs.start = next(random_node)
        greedy_best_fs.end = next(random_node)
        canvas_mock = mocker.Mock(spec=TestCanvas)
        mock_completed_path = mocker.patch.object(GreedyBestFS, 'completed_path')
        result = greedy_best_fs.execute()
        assert greedy_best_fs.open_set.not_empty
        mock_completed_path.assert_called()
        assert canvas_mock.draw
        assert result is True

    def test_execute_no_path(self, greedy_best_fs: GreedyBestFS, random_node: Generator[Node, None, None],
                             mocker: MockerFixture) -> None:
        greedy_best_fs.start = current = next(random_node)
        canvas_mock = mocker.Mock(spec=TestCanvas)
        mock_update_nonvisited = mocker.patch.object(current, 'update_nonvisited')
        result = greedy_best_fs.execute()
        assert greedy_best_fs.open_set.empty()
        mock_update_nonvisited.assert_called_with(greedy_best_fs.grid)
        assert current.visited
        assert canvas_mock.draw
        assert result is False
