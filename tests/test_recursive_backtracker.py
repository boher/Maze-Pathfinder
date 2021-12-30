import pytest
import colour
from typing import Generator
from pytest_mock import MockerFixture
from .test_algos import TestAlgos
from .test_canvas import TestCanvas
from algos.algos import Algos
from algos.recursive_backtracker import RecursiveBacktracker
from states.play import Play
from ui.node import Node


class TestRecursiveBacktracker(TestAlgos):

    # Arrange
    @pytest.fixture
    def recursive_backtracker(self, algos: Algos, mocker: MockerFixture) -> RecursiveBacktracker:
        canvas_mock = mocker.Mock(spec=TestCanvas)
        return RecursiveBacktracker(canvas_mock.draw, algos.grid, algos.start, algos.end, algos.speed, algos.auto_compute)

    # Act
    def test_put_stack(self, recursive_backtracker: RecursiveBacktracker, play_obj: Play) -> None:
        recursive_backtracker.start = recursive_backtracker.grid[play_obj.nav_height][play_obj.rect.top]
        recursive_backtracker.put_open_set()
        # Assert
        assert recursive_backtracker.open_set_hash == {recursive_backtracker.start}
        assert recursive_backtracker.stack.queue == [recursive_backtracker.start]

    def test_compare_neighbours(self, recursive_backtracker: RecursiveBacktracker, play_obj: Play,
                                random_node: Generator[Node, None, None], mocker: MockerFixture) -> None:
        mocker.patch.object(RecursiveBacktracker, 'set_speed')
        recursive_backtracker.start.row = play_obj.nav_height
        current = next(random_node)
        current.neighbours = [next(random_node), next(random_node), next(random_node), next(random_node)]
        recursive_backtracker.compare_neighbours(current)
        for neighbour in current.neighbours:
            assert neighbour in recursive_backtracker.open_set_hash
            assert neighbour in recursive_backtracker.stack.queue
        assert not current.get_start()
        assert not current.get_end()
        assert not recursive_backtracker.is_bomb(current)
        assert current.colour == colour.WHITE

    def test_execute(self, recursive_backtracker: RecursiveBacktracker, mocker: MockerFixture) -> None:
        canvas_mock = mocker.Mock(spec=TestCanvas)
        result = recursive_backtracker.execute()
        assert recursive_backtracker.stack.not_empty
        assert canvas_mock.draw
        assert result is True
