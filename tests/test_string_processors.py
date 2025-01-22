import pytest
from pathlib import Path

from src.lapko_bot.string_processors import fix

PATH_DIR_STRING_TEST_DATA = Path("tests/string_test_data")


def load_string_test_file(filename):
    with open(PATH_DIR_STRING_TEST_DATA / filename, "r", encoding="utf-8") as f:
        return f.read()


# Test cases (mapping input files to expected output files)
test_cases = [
    ("input_dash_1_1.txt", "output_dash_1_1.txt"),
    ("input_dash_a_1.txt", "output_dash_a_1.txt"),
    ("input_dash_a_a.txt", "output_dash_a_a.txt"),
    ("input_dash_direct.txt", "output_dash_direct.txt"),
    ("input_dash_i_i.txt", "output_dash_i_i.txt"),
    ("input_freeform.txt", "output_freeform.txt"),
    ("input_post.txt", "output_post.txt"),
]


@pytest.mark.parametrize("input_path, expected_path", test_cases)
def test_string_converter(input_path, expected_path):
    input_str = load_string_test_file(input_path)
    expected_output = load_string_test_file(expected_path)
    assert fix(input_str) == expected_output
