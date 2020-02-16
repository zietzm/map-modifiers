import functools
import json
import pytest

import map_modifiers.match


def load_vocab():
    with open('test/test_vocab.json', 'r') as f:
        return json.load(f)


@pytest.mark.parametrize('inputs,outputs', [
    (('ABC DEF GHI', 'GHI', 2), ['ABC DEF GHI']),
    (('abc def ghi', 'ghi', 2), ['abc def ghi']),
    (('abc def ghi', 'ghi', 1), ['def ghi']),
    (('abc def ghi', 'ghi', 0), ['ghi']),

    # Negative margins should return nothing
    (('abc def ghi', 'ghi', -1), []),
    (('abc def ghi', 'ghi', -2), []),

    # Margin should be as much as possible if the text has too few words.
    (('abc def ghi', 'ghi', 10), ['abc def ghi']),

    # No match
    (('abc def ghi', 'GHI', 3), []),
    (('abc def ghi', 'abcd', 3), []),

    # Match inside a word
    (('abc def ghi', 'e', 1), ['abc def ghi']),

    # ! Not sure what this should return
    # (('abc def ghi', ' ', 1), ['']),

    # Adversarial spaces within word function as expected
    (('abc def ghi', 'abc d', 2), ['abc def ghi']),
    (('abc def ghi', 'abc d', 5), ['abc def ghi']),
    (('abc def ghi', 'abc d', 0), ['abc def']),

    # Without normalization to remove newlines, tabs, etc.
    (('abc\ndef\tghi', 'e', 1), ['abc\ndef\tghi']),
    (('abc\ndef\tghi', 'e', 0), ['abc\ndef\tghi']),
])
def test_word_slice(inputs, outputs):
    assert map_modifiers.match.slice_word_margin(*inputs) == outputs


@pytest.mark.parametrize('string,margin_size,output', [
    # Margin size = 1
    (
        'patients must have abc', 1,
        [{'matched_term': 'abc', 'ID': '002', 'margin': 'have abc'}]
    ),
    # Margin size = 2
    (
        'patients must have abc', 2,
        [{'matched_term': 'abc', 'ID': '002', 'margin': 'must have abc'}]
    ),
    # Margin size = 3
    (
        'patients must have abc', 3,
        [{'matched_term': 'abc', 'ID': '002', 'margin': 'patients must have abc'}]
    ),
    # Multiple matches, margin size = 2
    (
        'patients having severe abc disorder and others', 2,
        [{'matched_term': 'abc', 'ID': '002',
          'margin': 'having severe abc disorder and'},
         {'matched_term': 'abc disorder', 'ID': '002',
          'margin': 'having severe abc disorder and others'},
         {'matched_term': 'severe abc disorder', 'ID': '001',
          'margin': 'patients having severe abc disorder and others'},
         ]
    ),
    # Multiple matches, margin size = 1
    (
        'patients having severe abc disorder and others', 1,
        [{'matched_term': 'abc', 'ID': '002',
          'margin': 'severe abc disorder'},
         {'matched_term': 'abc disorder', 'ID': '002',
          'margin': 'severe abc disorder and'},
         {'matched_term': 'severe abc disorder', 'ID': '001',
          'margin': 'having severe abc disorder and'},
         ]
    ),
    # Substring errors like this pass for simple match
    (
        'composers and painters and dancers', 1,
        [{'matched_term': 'pain', 'ID': '005', 'margin': 'and painters and'}]
    ),
])
def test_find_concept_occurrences(string, margin_size, output):
    term_to_id = load_vocab()
    word_margin_getter = functools.partial(
        map_modifiers.match.slice_word_margin,
        margin=margin_size)

    parsed_output = map_modifiers.match.find_term_occurrences(
        text_string=string,
        term_to_id=term_to_id,
        match_method=map_modifiers.match.match_simple,
        margin_method=word_margin_getter,
    )
    # All correct outputs were given
    for match in output:
        assert match in parsed_output

    # All given outputs were correct
    for match in parsed_output:
        assert match in output


@pytest.mark.parametrize('string,threshold,margin_size,match', [
    # One letter difference meets threshold=1
    ('abd', 1, 'abd', 'abc'),
    # One letter difference doesn't meet threshold=0
    ('abd', 0, '', ''),
    # One letter difference with longer string
    ('severe abd disorder', 1, 'severe abd disorder', 'severe abc disorder'),
    # Low thresholds exclude some incorrect substring matches
    ('composers and painters and dancers', 1, '', ''),
    # High thresholds permit some incorrect substring matches
    ('composers and painters and dancers', 100, 'painters', 'pain'),
])
def test_levenshtein_match(string, threshold, margin_size, match):
    term_to_id = load_vocab()
    matcher = functools.partial(map_modifiers.match.match_levenshtein,
                                threshold=threshold)
    word_margin_getter = functools.partial(
        map_modifiers.match.slice_word_margin,
        margin=margin_size)

    parsed_output = map_modifiers.match.find_term_occurrences(
        text_string=string,
        term_to_id=term_to_id,
        match_method=matcher,
        margin_method=word_margin_getter,
    )
    for parsed in parsed_output:
        assert parsed['margin'] == margin_size
        assert parsed['matched_term'] == match
