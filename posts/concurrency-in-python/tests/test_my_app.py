# test_my_app.py
import sys
import subprocess
from pathlib import Path
import pytest

import my_app


def test_greet_returns_expected_string():
    assert my_app.greet("Norbert") == "Hello, Norbert!"
    assert my_app.greet("World") == "Hello, World!"


@pytest.mark.parametrize(
    "a,b,expected",
    [
        (0, 0, 0),
        (1, 2, 3),
        (-1, 2, 1),
        (10**6, 10**6, 2 * 10**6),
    ],
)
def test_add_various_inputs(a, b, expected):
    assert my_app.add(a, b) == expected


def test_main_prints_expected_output(capsys):
    # Call main() directly and capture stdout.
    my_app.main()
    out = capsys.readouterr().out

    # Order matters; assert key lines are present.
    assert "Running my_app..." in out
    assert "Hello, Norbert!" in out
    assert "3 + 4 = 7" in out


def test_running_as_script_outputs_expected_lines(tmp_path):
    # Run "python my_app.py" as a subprocess to exercise the __main__ guard.
    script_path = Path(__file__).with_name("my_app.py")
    assert script_path.exists(), "my_app.py should be alongside this test file"

    proc = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    stdout = proc.stdout

    # Sanity checks on the script output
    assert "Running my_app..." in stdout
    assert "Hello, Norbert!" in stdout
    assert "3 + 4 = 7" in stdout
