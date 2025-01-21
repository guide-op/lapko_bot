# import pytest

from lapko_bot.string_processors import fix

test_data_ab = []
with open("tests/string_test_data.txt", "r", encoding="utf8") as f:
    # Mode = 0 - input, mode = 1 - output
    mode = 0
    io_pair = []
    entry = []
    for line in f:
        if line.strip() == ">>>":
            # Push input
            io_pair.append("\n".join(entry).strip())
            entry = []
            mode = 1
            continue
        if line.strip() == "===":
            # Push output, push in/out pair
            io_pair.append("\n".join(entry).strip())
            test_data_ab.append(io_pair)
            entry = []
            io_pair = []
            mode = 0
            continue
        entry.append(line.strip())


def test_quotify_001():
    a, b = test_data_ab[0]
    assert fix(a) == b


def test_quotify_002():
    a, b = test_data_ab[1]
    assert fix(a) == b


def test_quotify_003():
    a, b = test_data_ab[2]
    assert fix(a) == b


def test_quotify_with_empty_string():
    assert fix("") == ""


# def test_quotify_with_special_characters():
#     assert quotify("!@#$%^&*()") == '"!@#$%^&*()"'


# def test_quotify_with_none():
#     with pytest.raises(TypeError):
#         quotify(None)


# def test_quotify_with_list():
#     with pytest.raises(TypeError):
#         quotify([1, 2, 3])


# def test_quotify_with_dict():
#     with pytest.raises(TypeError):
#         quotify({"key": "value"})
