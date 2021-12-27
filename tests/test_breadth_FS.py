import pytest
import collections
from typing import Generator
from pytest_mock import MockerFixture
from .test_canvas import TestCanvas
from .test_algos import TestAlgos
from algos.algos import Algos
from algos.breadth_fs import BreadthFS
from ui.node import Node


class TestBreadthFS(TestAlgos):

    # Arrange
    @pytest.fixture
    def breadth_fs(self, algos: Algos, mocker: MockerFixture) -> BreadthFS:
        canvas_mock = mocker.Mock(spec=TestCanvas)
        return BreadthFS(canvas_mock.draw, algos.grid, algos.start, algos.end, algos.speed, algos.auto_compute)

    # Act
    def test_put_queue(self, breadth_fs: BreadthFS, random_node: Generator[Node, None, None]) -> None:
        breadth_fs.start = next(random_node)
        breadth_fs.put_open_set()
        # Assert
        assert breadth_fs.queue.queue == collections.deque([breadth_fs.start])
        assert breadth_fs.start.visited

    def test_compare_neighbours(self, breadth_fs: BreadthFS, random_node: Generator[Node, None, None],
                                mocker: MockerFixture) -> None:
        mocker.patch.object(BreadthFS, 'set_speed')
        mocker.patch.object(BreadthFS, 'manhattan_dist', return_value=12)
        current = next(random_node)
        current.neighbours = [next(random_node), next(random_node), next(random_node), next(random_node)]
        breadth_fs.compare_neighbours(current)
        for neighbour in current.neighbours:
            assert breadth_fs.came_from[neighbour] == current
            assert neighbour.visited
            assert neighbour != breadth_fs.end
            assert not neighbour.get_start()
            assert not neighbour.get_end()
            assert neighbour.get_open()

    def test_compare_neighbours_wall(self, breadth_fs: BreadthFS, random_node: Generator[Node, None, None]) -> None:
        current = next(random_node)
        neighbour_wall = next(random_node)
        neighbour_wall.set_wall()
        current.neighbours = [neighbour_wall]
        breadth_fs.compare_neighbours(current)
        assert current.neighbours.pop().get_wall()
        assert not neighbour_wall.get_open()

    def test_execute(self, breadth_fs: BreadthFS, random_node: Generator[Node, None, None], mocker: MockerFixture) -> None:
        breadth_fs.start = next(random_node)
        breadth_fs.end = next(random_node)
        canvas_mock = mocker.Mock(spec=TestCanvas)
        mock_completed_path = mocker.patch.object(BreadthFS, 'completed_path')
        result = breadth_fs.execute()
        assert breadth_fs.queue.not_empty
        mock_completed_path.assert_called()
        assert canvas_mock.draw
        assert result is True

    def test_execute_no_path(self, breadth_fs: BreadthFS, random_node: Generator[Node, None, None],
                             mocker: MockerFixture) -> None:
        breadth_fs.start = current = next(random_node)
        canvas_mock = mocker.Mock(spec=TestCanvas)
        mock_update_nonvisited = mocker.patch.object(current, 'update_nonvisited')
        result = breadth_fs.execute()
        mock_update_nonvisited.assert_called_with(breadth_fs.grid)
        assert breadth_fs.queue.empty()
        assert canvas_mock.draw
        assert result is False
