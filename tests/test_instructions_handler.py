import pytest
import pygame
from pytest_mock import MockerFixture
from states.instructions_handler import InstructionsHandler
from states.instructions import Instructions


class TestInstructionsHandler:

    # Arrange
    @pytest.fixture
    def instructions_handler(self) -> InstructionsHandler:
        return InstructionsHandler()

    # Act
    def test_instructions_handler_register(self, instructions_handler: InstructionsHandler) -> None:
        decorator = instructions_handler.register(pygame.MOUSEBUTTONDOWN)
        # Assert
        assert pygame.QUIT in instructions_handler.instructions_registry.keys()
        assert pygame.MOUSEBUTTONDOWN in instructions_handler.instructions_registry.keys()
        assert decorator.__name__ == "decorator"

    def test_instructions_quit(self, instructions: Instructions, mocker: MockerFixture) -> None:
        mock_pygame_quit = mocker.patch('pygame.quit')
        with pytest.raises(SystemExit):
            quit_event = pygame.event.Event(pygame.QUIT)
            InstructionsHandler.notify(instructions, quit_event)
            mock_pygame_quit.assert_called_once()

    def test_helper_close_btn_actions(self, instructions: Instructions, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch.object(instructions.close_btn, 'clicked', return_value=True)
        InstructionsHandler.notify(instructions, mouse_down_event)
        assert mouse_down_event.button == 1
        assert not instructions.instructions
        assert instructions.speed == 10

    def test_helper_forward_btn_actions(self, instructions: Instructions, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch.object(instructions.forward_btn, 'clicked', return_value=True)
        index_before = instructions.index
        InstructionsHandler.notify(instructions, mouse_down_event)
        assert mouse_down_event.button == 1
        assert instructions.index < 4
        assert instructions.index - index_before == 1

    def test_helper_back_btn_actions(self, instructions: Instructions, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mocker.patch.object(instructions.back_btn, 'clicked', return_value=True)
        index_before = instructions.index = 4
        InstructionsHandler.notify(instructions, mouse_down_event)
        assert mouse_down_event.button == 1
        assert instructions.index > 0
        assert index_before - instructions.index == 1

    def test_learn_more_maze_actions(self, instructions: Instructions, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mock_webbrowser_open = mocker.patch('webbrowser.open')
        mocker.patch.object(instructions.visualgo_resource, 'clicked', return_value=True)
        instructions.maze_options.active_option = 0
        instructions.path = False
        InstructionsHandler.notify(instructions, mouse_down_event)
        assert mouse_down_event.button == 1
        mock_webbrowser_open.assert_called_with(mocker.ANY)
        args, _ = mock_webbrowser_open.call_args
        maze_actions_url = args[0]
        assert "visualgo" in maze_actions_url

    def test_learn_more_pathfinding_actions(self, instructions: Instructions, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mock_webbrowser_open = mocker.patch('webbrowser.open')
        mocker.patch.object(instructions.visualgo_resource, 'clicked', return_value=True)
        instructions.pathfinding_options.active_option = 1
        instructions.path = True
        InstructionsHandler.notify(instructions, mouse_down_event)
        instructions.pathfinding_options.active_option = 2
        InstructionsHandler.notify(instructions, mouse_down_event)
        instructions.pathfinding_options.active_option = 3
        InstructionsHandler.notify(instructions, mouse_down_event)
        assert mouse_down_event.button == 1
        mock_webbrowser_open.assert_called_with(mocker.ANY)
        args, _ = mock_webbrowser_open.call_args
        pathfinding_actions_url = args[0]
        assert "visualgo" in pathfinding_actions_url

    def test_learn_more_landing_actions(self, instructions: Instructions, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mock_webbrowser_open = mocker.patch('webbrowser.open')
        mocker.patch.object(instructions.github_repo, 'clicked', return_value=True)
        InstructionsHandler.notify(instructions, mouse_down_event)
        assert mouse_down_event.button == 1
        mock_webbrowser_open.assert_called_with(mocker.ANY)
        args, _ = mock_webbrowser_open.call_args
        learn_more_landing_url = args[0]
        assert "github" in learn_more_landing_url

    def test_handson_maze_actions(self, instructions: Instructions, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mock_webbrowser_open = mocker.patch('webbrowser.open')
        mocker.patch.object(instructions.handson_resource, 'clicked', return_value=True)
        instructions.maze_options.active_option = 0
        instructions.maze = True
        InstructionsHandler.notify(instructions, mouse_down_event)
        assert mouse_down_event.button == 1
        mock_webbrowser_open.assert_called_with(mocker.ANY)
        args, _ = mock_webbrowser_open.call_args
        learn_more_handson_url = args[0]
        assert "mazes" in learn_more_handson_url

    def test_handson_pathfinding_actions(self, instructions: Instructions, mocker: MockerFixture) -> None:
        mouse_down_event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1)
        mock_webbrowser_open = mocker.patch('webbrowser.open')
        mocker.patch.object(instructions.handson_resource, 'clicked', return_value=True)
        instructions.pathfinding_options.active_option = 1
        instructions.path = True
        InstructionsHandler.notify(instructions, mouse_down_event)
        assert mouse_down_event.button == 1
        mock_webbrowser_open.assert_called_with(mocker.ANY)
        args, _ = mock_webbrowser_open.call_args
        learn_more_handson_url = args[0]
        assert "pathfinding" in learn_more_handson_url
