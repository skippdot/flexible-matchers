"""Flexible matchers for unittest.mock assertions.

This library provides flexible matcher objects that can be used in place of exact values
when asserting mock calls or comparing data structures in tests. All matchers use Python's
equality operators, so they work naturally with standard assertions.

Example:
    from flexible_matchers import NUMBER, STRING, IS_NUMBER, ANY_NOT_NONE

    # In mock assertions
    mock.assert_called_with(NUMBER(min_value=0, max_value=100), STRING(min_length=5))

    # In data structure comparisons
    assert response == {
        'id': IS_NUMBER,
        'name': STRING(min_length=1),
        'created_at': ANY_NOT_NONE
    }
"""

from typing import Union

__version__ = "0.1.0"
__all__ = [
    "NUMBER",
    "CLOSE_NUMBER",
    "STRING",
    "LIST",
    "ANY_NOT_NONE",
    "IS_NUMBER",
    "IS_STRING",
    "IS_LIST",
]


class NUMBER:
    """A matcher that compares numeric values with optional min/max constraints.

    Args:
        min_value: Minimum value (inclusive). If None, no minimum constraint.
        max_value: Maximum value (inclusive). If None, no maximum constraint.

    Example:
        >>> assert 42 == NUMBER()  # Any number
        >>> assert 42 == NUMBER(min_value=0)  # Non-negative
        >>> assert 42 == NUMBER(min_value=0, max_value=100)  # Range 0-100
        >>> assert 42 != NUMBER(min_value=50)  # Fails: 42 < 50
    """

    def __init__(
        self, min_value: Union[int, float] = None, max_value: Union[int, float] = None
    ):
        self.min = min_value
        self.max = max_value

    def __eq__(self, other: Union[int, float]) -> bool:
        return (
            type(other) in (int, float)
            and (self.min is None or other >= self.min)
            and (self.max is None or other <= self.max)
        )

    def __ne__(self, other: Union[int, float]) -> bool:
        return (
            type(other) not in (int, float)
            or (self.min is not None and other < self.min)
            or (self.max is not None and other > self.max)
        )

    def __repr__(self) -> str:
        if self.min is not None or self.max is not None:
            return f"<NUMBER({self.min}, {self.max})>"
        return "<NUMBER>"


class CLOSE_NUMBER:
    """A matcher that compares numbers with a tolerance for floating-point precision.

    Args:
        value: The expected value to compare against.
        tolerance: Maximum allowed difference (default: 0.5).

    Example:
        >>> assert 3.14 == CLOSE_NUMBER(3.1, tolerance=0.1)
        >>> assert 100 == CLOSE_NUMBER(99, tolerance=1)
        >>> assert 3.14 != CLOSE_NUMBER(3.5, tolerance=0.1)  # Fails: diff > 0.1
    """

    def __init__(self, value: Union[int, float], tolerance: float = 0.5):
        self.value = value
        self.tolerance = tolerance

    def __eq__(self, other: Union[int, float]) -> bool:
        return (
            type(other) in (int, float)
            and (self.value is None or abs(other - self.value) <= self.tolerance)
        )

    def __ne__(self, other: Union[int, float]) -> bool:
        return type(other) not in (int, float) or (
            self.value is not None and abs(other - self.value) > self.tolerance
        )

    def __str__(self) -> str:
        """String representation that just shows the value."""
        return str(self.value)

    def __repr__(self) -> str:
        """Representation that makes unittest diffs more readable."""
        return str(self.value)


class STRING:
    """A matcher that compares strings with optional length constraints.

    Args:
        length: Exact length required. If None, no exact length constraint.
        min_length: Minimum length (inclusive). If None, no minimum constraint.
        max_length: Maximum length (inclusive). If None, no maximum constraint.

    Example:
        >>> assert "hello" == STRING()  # Any string
        >>> assert "hello" == STRING(length=5)  # Exact length
        >>> assert "hello" == STRING(min_length=3, max_length=10)  # Length range
        >>> assert "hello" != STRING(min_length=10)  # Fails: len("hello") < 10
    """

    def __init__(
        self, length: int = None, min_length: int = None, max_length: int = None
    ):
        self.length = length
        self.min_length = min_length
        self.max_length = max_length

    def __eq__(self, other: str) -> bool:
        return (
            isinstance(other, str)
            and (self.length is None or len(other) == self.length)
            and (self.min_length is None or len(other) >= self.min_length)
            and (self.max_length is None or len(other) <= self.max_length)
        )

    def __ne__(self, other: str) -> bool:
        return not (
            isinstance(other, str)
            and (self.length is None or len(other) == self.length)
            and (self.min_length is None or len(other) >= self.min_length)
            and (self.max_length is None or len(other) <= self.max_length)
        )

    def __repr__(self) -> str:
        if (
            self.length is not None
            or self.min_length is not None
            or self.max_length is not None
        ):
            return f"<STRING({self.length}, {self.min_length}, {self.max_length})>"
        return "<STRING>"


class LIST:
    """A matcher that compares lists with optional length constraint.

    Args:
        length: Expected length. If None, matches any list.

    Example:
        >>> assert [1, 2, 3] == LIST()  # Any list
        >>> assert [1, 2, 3] == LIST(3)  # List with exactly 3 items
        >>> assert [1, 2, 3] != LIST(5)  # Fails: len != 5
    """

    def __init__(self, length: int = None):
        self.expected_length = length

    def __eq__(self, other: list) -> bool:
        if self.expected_length:
            return isinstance(other, list) and len(other) == self.expected_length
        return isinstance(other, list)

    def __ne__(self, other: list) -> bool:
        if self.expected_length:
            return not (isinstance(other, list) and len(other) == self.expected_length)
        return not isinstance(other, list)

    def __repr__(self) -> str:
        if self.expected_length is not None:
            return f"<LIST({self.expected_length})>"
        return "<LIST>"


class _AnyNotNone:
    """A matcher that equals any value except None.

    This is useful when you want to assert that a value exists but don't care
    about its specific value, similar to unittest.mock.ANY but excluding None.

    Example:
        >>> assert "hello" == ANY_NOT_NONE
        >>> assert 42 == ANY_NOT_NONE
        >>> assert [] == ANY_NOT_NONE
        >>> assert None != ANY_NOT_NONE  # Fails: None is not allowed
    """

    def __eq__(self, other):
        return other is not None

    def __ne__(self, other):
        return other is None

    def __repr__(self):
        return "ANY_NOT_NONE"


# Pre-instantiated matchers for common use cases
ANY_NOT_NONE = _AnyNotNone()
IS_NUMBER = NUMBER()
IS_STRING = STRING()
IS_LIST = LIST()
