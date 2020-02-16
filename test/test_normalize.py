import pytest

import map_modifiers.normalize


@pytest.mark.parametrize('inputs,outputs', [
    # Capitalization
    ('ABC', 'abc'),

    # Removes single characters leaving no trailing whitespace
    ('abc?', 'abc'),
    ('abc ?', 'abc'),

    # Leaves no more than one space in a row
    ('abc ? def', 'abc def'),

    # Remove newlines, tabs, leaving no trailing spaces
    ('\nabc\t?', 'abc'),

    # Removes all kinds of ASCII characters
    ('a,;"[]-=+_!!@#$%^&*()b', 'a b'),

    # Combination of several problems in one
    # ! Unclear whether "123ABC" should be "ABC" or "123abc"? Keep numbers in words?
    ('231a123, b;,c\td\n\n  \ne      f', 'a b c d e f'),
])
def test_normalize(inputs, outputs):
    assert map_modifiers.normalize.normalize(inputs) == outputs
