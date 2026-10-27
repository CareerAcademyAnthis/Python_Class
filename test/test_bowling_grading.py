import importlib
import os
from unittest.mock import patch
import pytest

STUDENT_FILE_DIR = "student_submissions"
STUDENT_MODULE_NAME = "chapter_9_challenge"

@pytest.fixture(scope="module")
def student_code():
    """Dynamically import the student's bowling module safely """
    file_path = os.path.join(STUDENT_FILE_DIR, f"{STUDENT_MODULE_NAME}.py")
    if not os.path.exists(file_path):
        pytest.fail(f"Could not find submission file '{file_path}.py")
    try:
        spec = importlib.util.spec_from_file_location(STUDENT_MODULE_NAME, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        pytest.fail(f"Student code failed to compile/import: {e}")


# ================================================================
# Archtecture test
#=================================================================

def test_oop_structure(student_code):
    """Verify that a student created classes for the assignment"""
    assert hasattr(student_code, "BowlingGame"), "Missing a main BowlingGame class"
    assert hasattr(student_code, "Frame"), "Missing a base Frame Class"
    #Verify that the created at least one subclass for special frame
    classes = [cls_name for cls_name in dir(student_code) if isinstance(getattr(student_code, cls_name), type)]
    assert len(classes) >= 3, f"Expected at least 3 classes (Game, Frame, Subclass), found: {classes}"


#=================================================================
# Functional Scoring Test (Frame by Frame)
#=================================================================

def test_terminal_gutter_game(student_main, capsys):
    """Feeds consecutive 0s into the terminal and reads the printed scoreboard."""

    # 20 consecutive inputs of '0' representing 10 frames of two missed rolls
    mock_inputs = ['0'] * 20

    # Intercept 'builtins.input' and feed it our list of strings sequentially
    with patch('builtins.input', side_effect=mock_inputs):
        student_main()

    # Capture what the student's program printed to the console
    captured = capsys.readouterr().out.lower()

    # Assertions: Verify the final printed scoreboard displays the correct progression
    assert "0" in captured, "The running score of 0 was never printed."


def test_terminal_open_frames(student_main, capsys):
    """Tests inputting a sequence of open frames with varying scores."""

    # Frame 1: 3, 4 (Total: 7) | Frame 2: 2, 5 (Total: 14) | Frame 3 through 10: all 0s
    mock_inputs = ['3', '4', '2', '5'] + (['0'] * 16)

    with patch('builtins.input', side_effect=mock_inputs):
        student_main()

    captured = capsys.readouterr().out

    # Check that both intermediate frame scores appear somewhere in the terminal output
    assert "7" in captured, "Failed to print or calculate score '7' after Frame 1."
    assert "14" in captured, "Failed to print or calculate cumulative score '14' after Frame 2."


def test_terminal_perfect_game(student_main, capsys):
    """Tests 12 consecutive entries of '10' for a perfect 300 game."""

    # 9 strikes for frames 1-9, plus 3 strikes for the 10th frame = 12 total inputs
    mock_inputs = ['10'] * 12

    with patch('builtins.input', side_effect=mock_inputs):
        student_main()

    captured = capsys.readouterr().out

    assert "300" in captured, "Perfect game total of 300 was not found in terminal outputs."
