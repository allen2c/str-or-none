import pytest


@pytest.mark.parametrize(
    "value, expected",
    [
        ("gg", "gg"),
        ("gg ", "gg"),
        (" gg ", "gg"),
        ("gg\n", "gg"),
    ],
)
def test_str_or_none(value, expected):
    import str_or_none

    assert str_or_none(value) == expected  # type: ignore


def test_str_or_none_func():
    from str_or_none import str_or_none

    assert str_or_none("\ngg\n") == "gg"
