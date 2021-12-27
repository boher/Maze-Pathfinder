import pytest
import colour
import random
from itertools import chain
from typing import Any, Generator, List, Tuple
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

    def test_draw_canvas(self, canvas: Canvas, grid: List[List[Node]], test_surface: surface.Surface,
                         mocker: MockerFixture) -> None:
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
            assert node.colour == colour.WHITE

    def test_reset_node_visited(self, canvas: Canvas, grid: List[List[Node]], random_node: Generator[Node, None, None]) -> None:
        start = next(random_node)
        end = next(random_node)
        bomb = next(random_node)
        canvas.reset_node_visited(grid, start, end, bomb)
        row = chain.from_iterable(grid)
        for node in row:
            if node is not start or node is not end or node is not bomb:
                assert node.visited is False

    def test_reset_traversed_path(self, canvas: Canvas, grid: List[List[Node]], random_node: Generator[Node, None, None]) -> None:
        start = next(random_node)
        end = next(random_node)
        bomb = next(random_node)
        grid = self.get_mock_traversed_node(grid)
        row = chain.from_iterable(grid)
        canvas.reset_traversed_path(grid, start, end, bomb)
        for node in row:
            assert node.colour == colour.WHITE

    def test_reset_walls(self, canvas: Canvas, grid: List[List[Node]]) -> None:
        row = chain.from_iterable(grid)
        for node in row:
            node.set_wall()
        canvas.reset_walls(grid)
        for node in row:
            assert node.colour == colour.WHITE

    def test_draw_canvas_as_walls(self, canvas: Canvas, grid: List[List[Node]], random_node: Generator[Node, None, None]) -> None:
        start = next(random_node)
        end = next(random_node)
        bomb = next(random_node)
        canvas.draw_canvas_as_walls(grid, start, end, bomb)
        row = chain.from_iterable(grid[canvas.nav_height:canvas.rows])
        for node in row:
            if node is not start and node is not end and node is not bomb:
                assert node.get_wall()
            assert not start.get_wall()
            assert not end.get_wall()
            assert not bomb.get_wall()

    @pytest.mark.parametrize('pos', [(random.randint(0, 99999), random.randint(0, 59)) for _ in range(5)])
    def test_fail_clicked_pos(self, canvas: Canvas, pos: Tuple[int, int]) -> None:
        with pytest.raises(IndexError):
            canvas.get_clicked_pos(pos)

    @pytest.mark.parametrize('pos', [(random.randint(0, 99999), random.randint(60, 99999)) for _ in range(5)])
    def test_get_clicked_pos(self, canvas: Canvas, pos: Tuple[int, int]) -> None:
        assert canvas.get_clicked_pos(pos)

    @staticmethod
    def get_mock_traversed_node(grid: List[List[Node]]) -> List[List[Node]]:
        row = chain.from_iterable(grid)
        # Divide and categorise to assign eligible node properties to test
        for index, node in enumerate(row):
            if index % 2:
                node.set_open()
            elif index % 3:
                node.set_closed()
            elif index % 5:
                node.set_bomb_closed()
            else:
                node.set_path()
        return grid
