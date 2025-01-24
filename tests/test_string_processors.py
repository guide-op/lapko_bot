import pytest
from pathlib import Path

from src.lapko_bot.string_processors import fix
from src.lapko_bot.string_processors import validate_quotes
from src.lapko_bot.helpers.enums import QuoteWarnings

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
    ("input_freeform_02.txt", "output_freeform_02.txt"),
    ("input_post.txt", "output_post.txt"),
]


# Test string conversion (without warnings)
@pytest.mark.parametrize("input_path, expected_path", test_cases)
def test_string_converter(input_path, expected_path):
    input_str = load_string_test_file(input_path)
    expected_output = load_string_test_file(expected_path)
    assert fix(input_str)[0] == expected_output


# Test quote validation
@pytest.mark.parametrize(
    "text, expected_warnings",
    [
        ("A «quote»", []),
        ("B «nested “quote”»", []),
        ("C «unclosed lquote", [(QuoteWarnings.QUOTE_UNCLOSED, 2)]),
        (
            "D «unclosed “nested quote»",
            [(QuoteWarnings.QUOTE_UNCLOSED, 2), (QuoteWarnings.QUOTE_MISMATCH, 25)],
        ),
        ("E unopened rquote»", [(QuoteWarnings.QUOTE_UNOPENED, 17)]),
        (
            "F «unopened nested” quote»",
            [(QuoteWarnings.QUOTE_MISMATCH, 18), (QuoteWarnings.QUOTE_UNOPENED, 25)],
        ),
        ("G «mismatched quote”", [(QuoteWarnings.QUOTE_MISMATCH, 19)]),
        ("H “mismatched quote»", [(QuoteWarnings.QUOTE_MISMATCH, 19)]),
        ("I «floating » rquote", [(QuoteWarnings.QUOTE_FLOATING, 12)]),
        (
            'J «floating " quote',
            [(QuoteWarnings.QUOTE_UNCLOSED, 2), (QuoteWarnings.QUOTE_FLOATING, 12)],
        ),
        (
            "K «double “unclosed",
            [(QuoteWarnings.QUOTE_UNCLOSED, 2), (QuoteWarnings.QUOTE_UNCLOSED, 10)],
        ),
        (
            "L double” unopened»",
            [(QuoteWarnings.QUOTE_UNOPENED, 8), (QuoteWarnings.QUOTE_UNOPENED, 18)],
        ),
    ],
)
def test_validate_quotes(text, expected_warnings):
    assert validate_quotes(text) == expected_warnings
