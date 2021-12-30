import pytest
import colour
from typing import Generator
from pytest_mock import MockerFixture
from .test_algos import TestAlgos
from .test_canvas import TestCanvas
from algos.algos import Algos
from ui.node import Node


class TestRecursiveBacktracker(TestAlgos):

    # Arrange
    @pytest.fixture
    def recursive_backtracker(self, algos: Algos, mocker: MockerFixture) -> Algos:
        canvas_mock = mocker.Mock(spec=TestCanvas)
        return Algos(canvas_mock.draw, algos.grid, algos.start, algos.end, algos.speed, algos.auto_compute)

    # Act
    def test_put_stack(self, recursive_backtracker: Algos) -> None:
        top_left_node = recursive_backtracker.start
        recursive_backtracker.put_open_set()
        # Assert
        assert recursive_backtracker.stack.queue == [top_left_node]

    def test_compare_neighbours(self, recursive_backtracker: Algos, random_node: Generator[Node, None, None],
                                mocker: MockerFixture) -> None:
        mocker.patch.object(Algos, 'set_speed')
        current = next(random_node)
        current.neighbours = [next(random_node), next(random_node), next(random_node), next(random_node)]
        recursive_backtracker.compare_neighbours(current)
        for neighbour in current.neighbours:
            assert neighbour in recursive_backtracker.stack.queue
        assert not current.get_start()
        assert not current.get_end()
        assert not recursive_backtracker.is_bomb(current)
        assert current.colour == colour.WHITE

    def test_execute(self, recursive_backtracker: Algos, mocker: MockerFixture) -> None:
        canvas_mock = mocker.Mock(spec=TestCanvas)
        assert recursive_backtracker.stack.not_empty
        assert canvas_mock.draw
