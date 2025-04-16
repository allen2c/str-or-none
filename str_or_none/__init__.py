# str_or_none/__init__.py
import datetime
import json
import sys
import types
import typing
from numbers import Number


def str_or_none(
    value: typing.Any, *, strip: bool = True, strict: bool = True
) -> typing.Optional[str]:
    if value is None:
        return None

    elif isinstance(value, typing.TextIO):
        _text = value.read()
        _text = _text.strip() if strip else _text
        return _text

    elif isinstance(value, typing.Text):
        _text = value
        _text = _text.strip() if strip else _text
        return _text

    elif isinstance(value, (int, float, bool, Number)):
        if strict:
            raise ValueError(
                f"Number cannot be converted to str in strict mode: {value}"
            )
        return str(value)

    elif isinstance(value, datetime.datetime):
        if strict:
            raise ValueError(
                f"Datetime cannot be converted to str in strict mode: {value}"
            )
        return value.isoformat()

    elif isinstance(
        value, (typing.List, typing.Tuple, typing.Sequence, typing.Iterable)
    ):
        if strict:
            raise ValueError(
                f"Sequence cannot be converted to str in strict mode: {value}"
            )
        return json.dumps(list(value), default=str)

    elif isinstance(value, (typing.Dict,)):
        if strict:
            raise ValueError(f"Dict cannot be converted to str in strict mode: {value}")
        return json.dumps(value, default=str)

    # __str__ or __repr__
    elif hasattr(value, "__str__") or hasattr(value, "__repr__"):
        if strict:
            raise ValueError(
                "Object with __str__ or __repr__ cannot be converted to str "
                + f"in strict mode: {value}"
            )
        return str(value).strip() if strip else str(value)

    else:
        raise ValueError(f"Cannot convert to str: {value}")


class CallableModule(types.ModuleType):
    def __call__(self, *args, **kwargs):
        return str_or_none(*args, **kwargs)


current_module = sys.modules[__name__]
current_module.__class__ = CallableModule


__all__ = ["str_or_none"]
__version__ = "0.1.0"
