# flexible-matchers

[![PyPI version](https://badge.fury.io/py/flexible-matchers.svg)](https://badge.fury.io/py/flexible-matchers)
[![Python Support](https://img.shields.io/pypi/pyversions/flexible-matchers.svg)](https://pypi.org/project/flexible-matchers/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Linting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/skippdot/flexible-matchers/workflows/CI/badge.svg)](https://github.com/skippdot/flexible-matchers/actions)
[![codecov](https://codecov.io/gh/skippdot/flexible-matchers/branch/main/graph/badge.svg)](https://codecov.io/gh/skippdot/flexible-matchers)

**Lightweight, zero-dependency mock assertion helpers with flexible numeric and string matching.**

`flexible-matchers` provides intuitive matcher objects for use with Python's `unittest.mock` and general test assertions. Unlike other matcher libraries, it uses Python's native equality operators, making it work seamlessly with standard assertions and mock calls.

## ✨ Key Features

- **🎯 Zero Dependencies** - No external packages required
- **�� Numeric Matchers** - Range-based and tolerance-based number matching
- **📝 String Matchers** - Flexible length constraints for string validation
- **📋 Collection Matchers** - List validation with length constraints
- **🚫 None Handling** - Special matcher for non-None values
- **🐍 Pythonic API** - Uses standard `==` operator, works with any assertion library
- **⚡ Lightweight** - Simple, focused implementation
- **🧪 Well-Tested** - Comprehensive test suite with 100% coverage
- **📦 Type-Hinted** - Full type annotations for better IDE support

## 🚀 Installation

```bash
pip install flexible-matchers
```

## 📖 Quick Start

```python
from flexible_matchers import NUMBER, STRING, IS_NUMBER, ANY_NOT_NONE

# In mock assertions
mock_api.assert_called_with(
    user_id=NUMBER(min_value=1),
    name=STRING(min_length=1),
    age=NUMBER(min_value=0, max_value=150)
)

# In data structure comparisons
response = {"id": 123, "name": "Alice", "created_at": "2024-01-01"}
assert response == {
    "id": IS_NUMBER,
    "name": STRING(min_length=1),
    "created_at": ANY_NOT_NONE
}
```

## 📚 Documentation

### NUMBER

Matches numeric values (int or float) with optional min/max constraints.

```python
from flexible_matchers import NUMBER, IS_NUMBER

# Match any number
assert 42 == NUMBER()
assert 3.14 == NUMBER()

# Match with minimum value
assert 42 == NUMBER(min_value=0)
assert -5 != NUMBER(min_value=0)

# Match with maximum value
assert 42 == NUMBER(max_value=100)
assert 150 != NUMBER(max_value=100)

# Match within range
assert 50 == NUMBER(min_value=0, max_value=100)
assert -1 != NUMBER(min_value=0, max_value=100)

# Pre-instantiated matcher for any number
assert 42 == IS_NUMBER
```

### CLOSE_NUMBER

Matches numbers within a tolerance range (useful for floating-point comparisons).

```python
from flexible_matchers import CLOSE_NUMBER

# Default tolerance of 0.5
assert 42.3 == CLOSE_NUMBER(42)
assert 41.7 == CLOSE_NUMBER(42)
assert 42.6 != CLOSE_NUMBER(42)

# Custom tolerance
assert 3.14 == CLOSE_NUMBER(3.1, tolerance=0.1)
assert 100 == CLOSE_NUMBER(99, tolerance=1)
```

**Unique Feature**: Unlike other libraries, `CLOSE_NUMBER` provides tolerance-based matching which is essential for floating-point comparisons in scientific computing and financial applications.

### STRING

Matches strings with optional length constraints.

```python
from flexible_matchers import STRING, IS_STRING

# Match any string
assert "hello" == STRING()
assert "" == STRING()

# Match exact length
assert "hello" == STRING(length=5)
assert "hi" != STRING(length=5)

# Match minimum length
assert "hello" == STRING(min_length=3)
assert "hi" != STRING(min_length=3)

# Match maximum length
assert "hello" == STRING(max_length=10)
assert "very long string" != STRING(max_length=10)

# Match length range
assert "hello" == STRING(min_length=3, max_length=10)

# Pre-instantiated matcher for any string
assert "hello" == IS_STRING
```

**Unique Feature**: Flexible string length constraints (`min_length`, `max_length`) are not available in most other matcher libraries.

### LIST

Matches lists with optional length constraint.

```python
from flexible_matchers import LIST, IS_LIST

# Match any list
assert [1, 2, 3] == LIST()
assert [] == LIST()

# Match exact length
assert [1, 2, 3] == LIST(3)
assert [1, 2] != LIST(3)

# Pre-instantiated matcher for any list
assert [1, 2, 3] == IS_LIST
```

### ANY_NOT_NONE

Matches any value except `None`.

```python
from flexible_matchers import ANY_NOT_NONE

# Matches any non-None value
assert 42 == ANY_NOT_NONE
assert "hello" == ANY_NOT_NONE
assert [] == ANY_NOT_NONE
assert 0 == ANY_NOT_NONE
assert False == ANY_NOT_NONE

# Does not match None
assert None != ANY_NOT_NONE
```

**Use Case**: Perfect for API responses where you want to ensure a field exists but don't care about its specific value.

## 🆚 Comparison with Other Libraries

### vs. unittest.mock.ANY

```python
from unittest.mock import ANY
from flexible_matchers import NUMBER, STRING

# unittest.mock.ANY - too permissive
assert {"age": -100} == {"age": ANY}  # Passes, but age is invalid!

# flexible-matchers - precise validation
assert {"age": 30} == {"age": NUMBER(min_value=0, max_value=150)}  # ✓
assert {"age": -100} == {"age": NUMBER(min_value=0, max_value=150)}  # ✗
```

### vs. PyHamcrest

```python
# PyHamcrest - requires special syntax
from hamcrest import assert_that, instance_of, greater_than
assert_that(value, instance_of(int))
assert_that(value, greater_than(0))

# flexible-matchers - natural Python syntax
from flexible_matchers import NUMBER
assert value == NUMBER(min_value=0)
```

### vs. dirty-equals

```python
# dirty-equals - close, but missing key features
from dirty_equals import IsPositiveInt
assert 42 == IsPositiveInt

# flexible-matchers - more flexible with ranges and tolerance
from flexible_matchers import NUMBER, CLOSE_NUMBER
assert 42 == NUMBER(min_value=0, max_value=100)
assert 3.14 == CLOSE_NUMBER(3.1, tolerance=0.1)  # Not available in dirty-equals
```

### vs. pychoir

```python
# pychoir - similar approach, but less intuitive
from pychoir import LessThan, GreaterThan, And
assert value == And(GreaterThan(0), LessThan(100))

# flexible-matchers - simpler, more intuitive
from flexible_matchers import NUMBER
assert value == NUMBER(min_value=0, max_value=100)
```

## 🎯 Real-World Examples

### API Testing

```python
from flexible_matchers import NUMBER, STRING, ANY_NOT_NONE

def test_create_user_api():
    response = api.create_user(name="Alice", email="alice@example.com")
    
    assert response == {
        "id": NUMBER(min_value=1),
        "name": STRING(min_length=1, max_length=100),
        "email": STRING(min_length=5),
        "created_at": ANY_NOT_NONE,
        "updated_at": ANY_NOT_NONE,
        "is_active": True,
    }
```

### Mock Assertions

```python
from unittest.mock import Mock
from flexible_matchers import NUMBER, STRING

def test_user_service():
    mock_db = Mock()
    service = UserService(mock_db)
    
    service.create_user(name="Alice", age=30)
    
    mock_db.insert.assert_called_once_with(
        table="users",
        data={
            "name": STRING(min_length=1),
            "age": NUMBER(min_value=0, max_value=150),
            "created_at": ANY_NOT_NONE,
        }
    )
```

### Nested Data Structures

```python
from flexible_matchers import NUMBER, STRING, LIST, IS_NUMBER

def test_complex_response():
    response = {
        "users": [
            {"id": 1, "name": "Alice", "scores": [95, 87, 92]},
            {"id": 2, "name": "Bob", "scores": [88, 91, 85]},
        ],
        "total": 2,
        "page": 1,
    }
    
    assert response == {
        "users": [
            {
                "id": IS_NUMBER,
                "name": STRING(min_length=1),
                "scores": LIST(3),
            },
            {
                "id": IS_NUMBER,
                "name": STRING(min_length=1),
                "scores": LIST(3),
            },
        ],
        "total": NUMBER(min_value=0),
        "page": NUMBER(min_value=1),
    }
```

### Floating-Point Comparisons

```python
from flexible_matchers import CLOSE_NUMBER

def test_scientific_calculation():
    result = calculate_pi()
    assert result == CLOSE_NUMBER(3.14159, tolerance=0.00001)
    
def test_financial_calculation():
    total = calculate_total([10.10, 20.20, 30.30])
    assert total == CLOSE_NUMBER(60.60, tolerance=0.01)
```

## 🛠️ Development

### Setup

```bash
# Clone the repository
git clone https://github.com/skippdot/flexible-matchers.git
cd flexible-matchers

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=flexible_matchers --cov-report=html

# Run specific test file
pytest tests/test_matchers.py

# Run specific test
pytest tests/test_matchers.py::TestNUMBER::test_range
```

### Code Quality

```bash
# Format code
black src tests
isort src tests

# Lint code
ruff check src tests
flake8 src tests
pylint src tests

# Type checking
mypy src
```

### Running All Checks

```bash
# Format
black src tests && isort src tests

# Lint
ruff check src tests && flake8 src tests && pylint src tests

# Test
pytest --cov=flexible_matchers --cov-report=term-missing

# Type check
mypy src
```

## 📋 Requirements

- Python >= 3.7
- No runtime dependencies!

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

Inspired by:
- [pychoir](https://github.com/kajaste/pychoir) - Modern matcher library
- [dirty-equals](https://github.com/samuelcolvin/dirty-equals) - Flexible equality testing
- [PyHamcrest](https://github.com/hamcrest/PyHamcrest) - Mature matcher framework
- [callee](https://github.com/Xion/callee) - Argument matchers (now abandoned)

## 📊 Project Stats

- **Zero Dependencies**: No external packages required
- **100% Test Coverage**: Comprehensive test suite
- **Type Hinted**: Full type annotations
- **Python 3.7+**: Modern Python support
- **Active Maintenance**: Regular updates and improvements

## 🔗 Links

- **PyPI**: https://pypi.org/project/flexible-matchers/
- **GitHub**: https://github.com/skippdot/flexible-matchers
- **Issues**: https://github.com/skippdot/flexible-matchers/issues
- **Changelog**: https://github.com/skippdot/flexible-matchers/releases

---

Made with ❤️ by [Stepan Shamaiev](https://github.com/skippdot)
