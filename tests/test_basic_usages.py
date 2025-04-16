import datetime
import io
import json

import pytest


class CustomStr:
    def __str__(self):
        return "custom_str_repr"


@pytest.mark.parametrize(
    "value, expected, kwargs, raises",
    [
        ("gg", "gg", {}, None),
        ("gg ", "gg", {}, None),
        (" gg ", "gg", {}, None),
        ("gg\n", "gg", {}, None),
        (None, None, {}, None),
        (io.StringIO("  hello  "), "hello", {}, None),
        (io.StringIO("  hello  "), "  hello  ", {"strip": False}, None),
        ("  hello  ", "  hello  ", {"strip": False}, None),
        (123, None, {}, ValueError),
        (123, "123", {"strict": False}, None),
        (12.34, None, {}, ValueError),
        (12.34, "12.34", {"strict": False}, None),
        (True, None, {}, ValueError),
        (True, "True", {"strict": False}, None),
        (datetime.datetime(2020, 1, 1, 12, 0), None, {}, ValueError),
        (
            datetime.datetime(2020, 1, 1, 12, 0),
            "2020-01-01T12:00:00",
            {"strict": False},
            None,
        ),
        ([1, 2, 3], None, {}, ValueError),
        ([1, 2, 3], json.dumps([1, 2, 3]), {"strict": False}, None),
        ((1, 2), None, {}, ValueError),
        ((1, 2), json.dumps([1, 2]), {"strict": False}, None),
        ({"a": 1}, None, {}, ValueError),
        ({"a": 1}, json.dumps({"a": 1}), {"strict": False}, None),
        (set([1, 2]), None, {}, ValueError),
        (set([1, 2]), json.dumps(sorted([1, 2])), {"strict": False}, None),
        (CustomStr(), None, {}, ValueError),
        (CustomStr(), "custom_str_repr", {"strict": False, "strip": False}, None),
        (CustomStr(), "custom_str_repr", {"strict": False}, None),
    ],
)
def test_str_or_none(value, expected, kwargs, raises):
    import str_or_none

    if raises:
        with pytest.raises(raises):
            str_or_none(value, **kwargs)  # type: ignore
    else:
        assert str_or_none(value, **kwargs) == expected  # type: ignore


def test_str_or_none_func():
    from str_or_none import str_or_none

    assert str_or_none("\ngg\n") == "gg"
