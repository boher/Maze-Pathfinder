import pytest
from typing import Generator
from pytest_mock import MockerFixture
from .test_canvas import TestCanvas
from .test_algos import TestAlgos
from algos.algos import Algos
from algos.depth_fs import DepthFS
from ui.node import Node


class TestDepthFS(TestAlgos):

    # Arrange
    @pytest.fixture
    def depth_fs(self, algos: Algos, mocker: MockerFixture) -> DepthFS:
        canvas_mock = mocker.Mock(spec=TestCanvas)
        return DepthFS(canvas_mock.draw, algos.grid, algos.start, algos.end, algos.speed, algos.auto_compute)

    # Act
    def test_put_stack(self, depth_fs: DepthFS, random_node: Generator[Node, None, None]) -> None:
        depth_fs.start = next(random_node)
        depth_fs.put_open_set()
        # Assert
        assert depth_fs.stack.queue == [depth_fs.start]
        assert depth_fs.start.visited

    def test_compare_neighbours(self, depth_fs: DepthFS, random_node: Generator[Node, None, None],
                                mocker: MockerFixture) -> None:
        mocker.patch.object(DepthFS, 'set_speed')
        mocker.patch.object(DepthFS, 'manhattan_dist', return_value=12)
        current = next(random_node)
        current.neighbours = [next(random_node), next(random_node), next(random_node), next(random_node)]
        depth_fs.compare_neighbours(current)
        for neighbour in current.neighbours:
            assert depth_fs.came_from[neighbour] == current
            assert neighbour.visited
            assert neighbour != depth_fs.end
            assert not neighbour.get_start()
            assert not neighbour.get_end()
            assert neighbour.get_open()

    def test_compare_neighbours_wall(self, depth_fs: DepthFS, random_node: Generator[Node, None, None]) -> None:
        current = next(random_node)
        neighbour_wall = next(random_node)
        neighbour_wall.set_wall()
        current.neighbours = [neighbour_wall]
        depth_fs.compare_neighbours(current)
        assert current.neighbours.pop().get_wall()
        assert not neighbour_wall.get_open()

    def test_execute(self, depth_fs: DepthFS, random_node: Generator[Node, None, None], mocker: MockerFixture) -> None:
        depth_fs.start = next(random_node)
        depth_fs.end = next(random_node)
        canvas_mock = mocker.Mock(spec=TestCanvas)
        mock_completed_path = mocker.patch.object(DepthFS, 'completed_path')
        result = depth_fs.execute()
        assert depth_fs.stack.not_empty
        mock_completed_path.assert_called()
        assert canvas_mock.draw
        assert result is True

    def test_execute_no_path(self, depth_fs: DepthFS, random_node: Generator[Node, None, None],
                             mocker: MockerFixture) -> None:
        depth_fs.start = current = next(random_node)
        canvas_mock = mocker.Mock(spec=TestCanvas)
        mock_update_nonvisited = mocker.patch.object(current, 'update_nonvisited')
        result = depth_fs.execute()
        mock_update_nonvisited.assert_called_with(depth_fs.grid)
        assert depth_fs.stack.empty()
        assert canvas_mock.draw
        assert result is False
