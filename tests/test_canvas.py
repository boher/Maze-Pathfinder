import pytest
import colour
import random
from itertools import chain
from typing import Any, List, Tuple
from pytest_mock import MockerFixture
from pygame import surface
from ui.node import Node
from ui.canvas import Canvas


class TestCanvas:

    # Arrange
    @pytest.fixture(scope="module")
    def canvas(self) -> Canvas:
        return Canvas()

    @pytest.fixture(name="draw")
    def draw(self, canvas: Canvas, grid: List[List[Node]]) -> Any:
        return canvas.draw_canvas(grid=grid)

    # Act
    def test_draw_grid(self, canvas: Canvas) -> None:
        grid = canvas.create_grid()
        # Assert
        assert len(grid) == canvas.rows
        assert len(grid[0]) == canvas.cols
        row = chain.from_iterable(grid)
        for node in row:
            assert isinstance(node, Node)

    def test_create_grid(self, canvas: Canvas) -> None:
        assert canvas.create_grid()

    def test_draw_canvas(self, canvas: Canvas, grid: List[List[Node]], test_surface: surface.Surface, mocker: MockerFixture) -> None:
        canvas.screen = test_surface
        mocker.patch('pygame.draw.line')
        canvas.draw_canvas(grid)
        assert test_surface.fill(colour.WHITE)

    def test_node_traversal(self, canvas: Canvas, grid: List[List[Node]]) -> None:
        canvas.node_traversal(grid)
        row = chain.from_iterable(grid)
        for node in row:
            node.update_neighbours(grid)
            assert node.neighbours is not None

    def test_reset_open_nodes(self, canvas: Canvas, grid: List[List[Node]]) -> None:
        canvas.reset_open_nodes(grid)
        row = chain.from_iterable(grid)
        for node in row:
            assert node.reset

    def test_reset_node_visited(self, canvas: Canvas, grid: List[List[Node]], mocker: MockerFixture) -> None:
        start = mocker.Mock(spec=Node)
        end = mocker.Mock(spec=Node)
        bomb = mocker.Mock(spec=Node)
        canvas.reset_node_visited(grid, start, end, bomb)
        row = chain.from_iterable(grid)
        for node in row:
            if node is not start or node is not end or node is not bomb:
                assert node.visited is False

    def test_reset_traversed_path(self, canvas: Canvas, grid: List[List[Node]], mocker: MockerFixture) -> None:
        start = mocker.Mock(spec=Node)
        end = mocker.Mock(spec=Node)
        bomb = mocker.Mock(spec=Node)
        row = chain.from_iterable(grid)
        for node in row:
            node.colour = colour.MAGENTA
        canvas.reset_traversed_path(grid, start, end, bomb)

    def test_reset_walls(self, canvas: Canvas, grid: List[List[Node]]) -> None:
        row = chain.from_iterable(grid)
        for node in row:
            node.set_wall()
        canvas.reset_walls(grid)

    @pytest.mark.parametrize('pos', [(random.randint(0, 99999), random.randint(0, 59)) for _ in range(5)])
    def test_fail_clicked_pos(self, canvas: Canvas, pos: Tuple[int, int]) -> None:
        with pytest.raises(IndexError):
            canvas.get_clicked_pos(pos)

    @pytest.mark.parametrize('pos', [(random.randint(0, 99999), random.randint(0, 99999)) for _ in range(5)])
    def test_get_clicked_pos(self, canvas: Canvas, pos: Tuple[int, int]) -> None:
        assert canvas.get_clicked_pos(pos)
