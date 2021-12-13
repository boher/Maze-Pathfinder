from pytest_mock import MockerFixture
from states.play import Play


class TestInstructions:

    # Act
    def test_blit_newlines(self, play_obj: Play) -> None:
        play_obj.blit_newlines("Some play_obj", play_obj.length, play_obj.width)
        # Assert
        assert play_obj.font.render
        assert play_obj.screen.blit

    def test_blit_newlines_short_surface_width(self, play_obj: Play) -> None:
        play_obj.blit_newlines("Surface width shorter than length", play_obj.cols, play_obj.width)
        assert play_obj.font.render
        assert play_obj.screen.blit

    def test_get_handson_resource_maze(self, play_obj: Play) -> None:
        play_obj.maze_options.active_option = 2
        play_obj.get_handson_resource_text()
        assert "Maze" in play_obj.get_handson_resource_text()

    def test_get_handson_resource_pathfinding(self, play_obj: Play) -> None:
        play_obj.path = True
        play_obj.pathfinding_options.active_option = 2
        play_obj.get_handson_resource_text()
        assert "Pathfinding" in play_obj.get_handson_resource_text()

    def test_get_learn_more_landing(self, play_obj: Play) -> None:
        play_obj.index = 3
        play_obj.get_learn_more()
        assert play_obj.path is False
        assert play_obj.maze_options.active_option == -1
        assert play_obj.pathfinding_options.active_option == -1

    def test_get_learn_more_pathfinding(self, play_obj: Play) -> None:
        play_obj.index = 3
        play_obj.path = True
        play_obj.pathfinding_options.active_option = 2
        play_obj.get_learn_more()
        assert play_obj.pathfinding_options.active_option > -1

    def test_get_play_obj(self, play_obj: Play) -> None:
        instructions_text = play_obj.get_instructions()
        assert play_obj.index == 0
        if instructions_text is not None:
            assert "maze generation" and "pathfinding algorithms" in instructions_text

    def test_popup_helper(self, play_obj: Play, mocker: MockerFixture) -> None:
        mock_blit_newlines = mocker.patch.object(Play, 'blit_newlines')
        mocker.patch('pygame.event.get', return_value=[])  # No instructions events handled
        assert play_obj.instructions is True
        mocker.patch('pygame.display.update', side_effect=lambda: setattr(play_obj, 'instructions', False))
        play_obj.popup_helper()
        mock_blit_newlines.assert_called()
        assert play_obj.instructions is False
