"""Comprehensive tests for flexible_matchers."""

# pylint: disable=singleton-comparison, use-implicit-booleaness-not-comparison

from flexible_matchers import (
    ANY_NOT_NONE,
    CLOSE_NUMBER,
    IS_LIST,
    IS_NUMBER,
    IS_STRING,
    LIST,
    NUMBER,
    STRING,
)


class TestNUMBER:
    """Tests for the NUMBER matcher."""

    def test_any_number(self):
        """Test NUMBER() matches any numeric value."""
        assert 42 == NUMBER()
        assert 3.14 == NUMBER()
        assert -100 == NUMBER()
        assert 0 == NUMBER()

    def test_not_a_number(self):
        """Test NUMBER() does not match non-numeric values."""
        assert "42" != NUMBER()
        assert None != NUMBER()
        assert [] != NUMBER()
        assert {} != NUMBER()

    def test_min_value(self):
        """Test NUMBER with minimum value constraint."""
        assert 42 == NUMBER(min_value=0)
        assert 42 == NUMBER(min_value=42)
        assert 42 != NUMBER(min_value=43)
        assert 0 == NUMBER(min_value=0)
        assert -1 != NUMBER(min_value=0)

    def test_max_value(self):
        """Test NUMBER with maximum value constraint."""
        assert 42 == NUMBER(max_value=100)
        assert 42 == NUMBER(max_value=42)
        assert 42 != NUMBER(max_value=41)
        assert 0 == NUMBER(max_value=0)
        assert 1 != NUMBER(max_value=0)

    def test_range(self):
        """Test NUMBER with both min and max constraints."""
        assert 50 == NUMBER(min_value=0, max_value=100)
        assert 0 == NUMBER(min_value=0, max_value=100)
        assert 100 == NUMBER(min_value=0, max_value=100)
        assert -1 != NUMBER(min_value=0, max_value=100)
        assert 101 != NUMBER(min_value=0, max_value=100)

    def test_repr(self):
        """Test NUMBER string representation."""
        assert repr(NUMBER()) == "<NUMBER>"
        assert repr(NUMBER(min_value=0)) == "<NUMBER(0, None)>"
        assert repr(NUMBER(max_value=100)) == "<NUMBER(None, 100)>"
        assert repr(NUMBER(min_value=0, max_value=100)) == "<NUMBER(0, 100)>"

    def test_is_number_instance(self):
        """Test pre-instantiated IS_NUMBER."""
        assert 42 == IS_NUMBER
        assert 3.14 == IS_NUMBER
        assert "42" != IS_NUMBER


class TestCLOSE_NUMBER:
    """Tests for the CLOSE_NUMBER matcher."""

    def test_exact_match(self):
        """Test CLOSE_NUMBER with exact value."""
        assert 42 == CLOSE_NUMBER(42)
        assert 3.14 == CLOSE_NUMBER(3.14)

    def test_within_tolerance(self):
        """Test CLOSE_NUMBER within default tolerance."""
        assert 42.3 == CLOSE_NUMBER(42)
        assert 41.7 == CLOSE_NUMBER(42)
        assert 42.5 == CLOSE_NUMBER(42)
        assert 41.5 == CLOSE_NUMBER(42)

    def test_outside_tolerance(self):
        """Test CLOSE_NUMBER outside default tolerance."""
        assert 42.6 != CLOSE_NUMBER(42)
        assert 41.4 != CLOSE_NUMBER(42)

    def test_custom_tolerance(self):
        """Test CLOSE_NUMBER with custom tolerance."""
        assert 42.9 == CLOSE_NUMBER(42, tolerance=1.0)
        assert 41.1 == CLOSE_NUMBER(42, tolerance=1.0)
        assert 43.1 != CLOSE_NUMBER(42, tolerance=1.0)
        assert 40.9 != CLOSE_NUMBER(42, tolerance=1.0)

    def test_small_tolerance(self):
        """Test CLOSE_NUMBER with small tolerance."""
        assert 3.14 == CLOSE_NUMBER(3.14, tolerance=0.01)
        assert 3.15 == CLOSE_NUMBER(3.14, tolerance=0.01)  # Exactly at boundary (inclusive)
        assert 3.151 != CLOSE_NUMBER(3.14, tolerance=0.01)  # Outside tolerance
        assert 3.129 != CLOSE_NUMBER(3.14, tolerance=0.01)  # Outside tolerance

    def test_not_a_number(self):
        """Test CLOSE_NUMBER does not match non-numeric values."""
        assert "42" != CLOSE_NUMBER(42)
        assert None != CLOSE_NUMBER(42)
        assert [] != CLOSE_NUMBER(42)

    def test_repr(self):
        """Test CLOSE_NUMBER string representation."""
        assert str(CLOSE_NUMBER(42)) == "42"
        assert repr(CLOSE_NUMBER(42)) == "42"
        assert str(CLOSE_NUMBER(3.14)) == "3.14"


class TestSTRING:
    """Tests for the STRING matcher."""

    def test_any_string(self):
        """Test STRING() matches any string."""
        assert "hello" == STRING()
        assert "" == STRING()
        assert "a" == STRING()
        assert "very long string" == STRING()

    def test_not_a_string(self):
        """Test STRING() does not match non-string values."""
        assert 42 != STRING()
        assert None != STRING()
        assert [] != STRING()
        assert {} != STRING()

    def test_exact_length(self):
        """Test STRING with exact length constraint."""
        assert "hello" == STRING(length=5)
        assert "hi" == STRING(length=2)
        assert "" == STRING(length=0)
        assert "hello" != STRING(length=4)
        assert "hello" != STRING(length=6)

    def test_min_length(self):
        """Test STRING with minimum length constraint."""
        assert "hello" == STRING(min_length=3)
        assert "hello" == STRING(min_length=5)
        assert "hello" != STRING(min_length=6)
        assert "" != STRING(min_length=1)

    def test_max_length(self):
        """Test STRING with maximum length constraint."""
        assert "hello" == STRING(max_length=10)
        assert "hello" == STRING(max_length=5)
        assert "hello" != STRING(max_length=4)
        assert "" == STRING(max_length=0)

    def test_length_range(self):
        """Test STRING with both min and max constraints."""
        assert "hello" == STRING(min_length=3, max_length=10)
        assert "hi" != STRING(min_length=3, max_length=10)
        assert "very long string" != STRING(min_length=3, max_length=10)

    def test_repr(self):
        """Test STRING string representation."""
        assert repr(STRING()) == "<STRING>"
        assert repr(STRING(length=5)) == "<STRING(5, None, None)>"
        assert repr(STRING(min_length=3)) == "<STRING(None, 3, None)>"
        assert repr(STRING(max_length=10)) == "<STRING(None, None, 10)>"
        assert repr(STRING(min_length=3, max_length=10)) == "<STRING(None, 3, 10)>"

    def test_is_string_instance(self):
        """Test pre-instantiated IS_STRING."""
        assert "hello" == IS_STRING
        assert "" == IS_STRING
        assert 42 != IS_STRING


class TestLIST:
    """Tests for the LIST matcher."""

    def test_any_list(self):
        """Test LIST() matches any list."""
        assert [] == LIST()
        assert [1] == LIST()
        assert [1, 2, 3] == LIST()
        assert ["a", "b", "c"] == LIST()

    def test_not_a_list(self):
        """Test LIST() does not match non-list values."""
        assert 42 != LIST()
        assert "list" != LIST()
        assert None != LIST()
        assert {} != LIST()
        assert (1, 2, 3) != LIST()

    def test_exact_length(self):
        """Test LIST with exact length constraint."""
        assert [] == LIST(0)
        assert [1] == LIST(1)
        assert [1, 2, 3] == LIST(3)
        assert [1, 2, 3] != LIST(2)
        assert [1, 2, 3] != LIST(4)

    def test_repr(self):
        """Test LIST string representation."""
        assert repr(LIST()) == "<LIST>"
        assert repr(LIST(3)) == "<LIST(3)>"
        assert repr(LIST(0)) == "<LIST(0)>"

    def test_is_list_instance(self):
        """Test pre-instantiated IS_LIST."""
        assert [] == IS_LIST
        assert [1, 2, 3] == IS_LIST
        assert "list" != IS_LIST


class TestANY_NOT_NONE:
    """Tests for the ANY_NOT_NONE matcher."""

    def test_matches_any_value(self):
        """Test ANY_NOT_NONE matches any non-None value."""
        assert 42 == ANY_NOT_NONE
        assert "hello" == ANY_NOT_NONE
        assert [] == ANY_NOT_NONE
        assert {} == ANY_NOT_NONE
        assert 0 == ANY_NOT_NONE
        assert "" == ANY_NOT_NONE
        assert False == ANY_NOT_NONE

    def test_does_not_match_none(self):
        """Test ANY_NOT_NONE does not match None."""
        assert None != ANY_NOT_NONE

    def test_repr(self):
        """Test ANY_NOT_NONE string representation."""
        assert repr(ANY_NOT_NONE) == "ANY_NOT_NONE"


class TestIntegration:
    """Integration tests with complex data structures."""

    def test_dict_matching(self):
        """Test matchers in dictionary comparisons."""
        data = {"id": 123, "name": "John", "age": 30}
        assert data == {"id": IS_NUMBER, "name": IS_STRING, "age": NUMBER(min_value=0)}

    def test_list_matching(self):
        """Test matchers in list comparisons."""
        data = [1, 2, 3, 4, 5]
        assert data == [IS_NUMBER, IS_NUMBER, IS_NUMBER, IS_NUMBER, IS_NUMBER]

    def test_nested_structures(self):
        """Test matchers in nested data structures."""
        data = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"},
            ],
            "count": 2,
        }
        assert data == {
            "users": [
                {"id": IS_NUMBER, "name": STRING(min_length=1)},
                {"id": IS_NUMBER, "name": STRING(min_length=1)},
            ],
            "count": NUMBER(min_value=0),
        }

    def test_with_any_not_none(self):
        """Test ANY_NOT_NONE in complex structures."""
        data = {"id": 123, "created_at": "2024-01-01", "updated_at": None}
        assert data == {
            "id": ANY_NOT_NONE,
            "created_at": ANY_NOT_NONE,
            "updated_at": None,
        }
