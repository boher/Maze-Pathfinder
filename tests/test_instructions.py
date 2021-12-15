from pytest_mock import MockerFixture
from states.instructions import Instructions


class TestInstructions:

    # Act
    def test_blit_newlines(self, instructions: Instructions) -> None:
        instructions.blit_newlines("Some play_obj", instructions.length, instructions.width)
        # Assert
        assert instructions.font.render
        assert instructions.screen.blit

    def test_blit_newlines_short_surface_width(self, instructions: Instructions) -> None:
        instructions.blit_newlines("Surface width shorter than length", instructions.cols, instructions.width)
        assert instructions.font.render
        assert instructions.screen.blit

    def test_get_handson_resource_maze(self, instructions: Instructions) -> None:
        instructions.maze_options.active_option = 2
        instructions.get_handson_resource_text()
        assert "Maze" in instructions.get_handson_resource_text()

    def test_get_handson_resource_pathfinding(self, instructions: Instructions) -> None:
        instructions.path = True
        instructions.pathfinding_options.active_option = 2
        instructions.get_handson_resource_text()
        assert "Pathfinding" in instructions.get_handson_resource_text()

    def test_get_learn_more_landing(self, instructions: Instructions) -> None:
        instructions.index = 3
        instructions.get_learn_more()
        assert instructions.path is False
        assert instructions.maze_options.active_option == -1
        assert instructions.pathfinding_options.active_option == -1

    def test_get_learn_more_pathfinding(self, instructions: Instructions) -> None:
        instructions.index = 3
        instructions.path = True
        instructions.pathfinding_options.active_option = 2
        instructions.get_learn_more()
        assert instructions.pathfinding_options.active_option > -1

    def test_get_play_obj(self, instructions: Instructions) -> None:
        instructions_text = instructions.get_instructions()
        assert instructions.index == 0
        if instructions_text is not None:
            assert "maze generation" and "pathfinding algorithms" in instructions_text

    def test_popup_helper(self, instructions: Instructions, mocker: MockerFixture) -> None:
        mock_blit_newlines = mocker.patch.object(Instructions, 'blit_newlines')
        mocker.patch('pygame.event.get', return_value=[])  # No instructions events handled
        assert instructions.instructions is True
        mocker.patch('pygame.display.update', side_effect=lambda: setattr(instructions, 'instructions', False))
        instructions.popup_helper()
        mock_blit_newlines.assert_called()
        assert instructions.instructions is False
