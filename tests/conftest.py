import os
import pytest
import pygame
from types import ModuleType
from typing import Generator
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
def grid(play_obj: Play):
    return [[Node(row, col, play_obj.gap, (play_obj.rows, play_obj.cols)) for col in range(play_obj.cols)] for row in
            range(play_obj.rows)]


@pytest.fixture
def play_obj() -> Play:
    return Play()
