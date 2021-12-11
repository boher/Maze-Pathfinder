import os
import pytest
import pygame
import random
from types import ModuleType
from typing import Generator, List
from states.play import Play
from ui.node import Node


@pytest.fixture(scope="module", autouse=True)
def init_pygame() -> Generator[ModuleType, None, None]:
    # Setup
    os.environ["SDL_VIDEODRIVER"] = "dummy"
    os.environ["SDL_AUDIODRIVER"] = "dummy"
    pygame.init()
    yield pygame
    # Teardown
    pygame.quit()


@pytest.fixture
def test_surface(play_obj: Play) -> Generator[pygame.surface.Surface, None, None]:
    screen = pygame.display.set_mode((1, 1), 0, play_obj.rows)
    yield screen
    pygame.display.quit()


@pytest.fixture
def test_surface_yield_none(play_obj: Play) -> Generator[None, None, None]:
    pygame.display.set_mode((1, 1), 0, play_obj.rows)
    yield None
    pygame.display.quit()


@pytest.fixture
def grid(play_obj: Play) -> List[List[Node]]:
    return [[Node(row, col, play_obj.gap, (play_obj.rows, play_obj.cols)) for col in range(play_obj.cols)] for row in
            range(play_obj.rows)]


@pytest.fixture(autouse=True)
def random_node(grid: List[List[Node]]) -> Generator[Node, None, None]:
    def generate_random_node(grid: List[List[Node]]) -> Generator[Node, None, None]:
        all_nodes = [node for row in grid for node in row]
        for _ in all_nodes:
            yield random.sample(all_nodes, 1)[0]
    return generate_random_node(grid)


@pytest.fixture
def play_obj() -> Play:
    return Play()
