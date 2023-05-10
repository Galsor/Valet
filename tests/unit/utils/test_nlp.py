import pytest

from src.utils.nlp import is_question


@pytest.mark.parametrize(
    "text, expected",
    [
        ("Where are you?", True),
        ("https://somesite.com/q/95858?who=john", False),
        ("Hello, comment va? Moi pas mal", True),
    ],
)
def test_is_question(text, expected):
    assert is_question(text) == expected
