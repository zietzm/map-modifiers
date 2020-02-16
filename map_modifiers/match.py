import re
from typing import Callable, Dict, List

import map_modifiers.similarity


def find_term_occurrences(
        text_string: str,
        term_to_id: Dict[str, str],
        match_method: Callable[[str, str], bool],
        margin_method: Callable[[str, str], List[str]]) -> List[Dict[str, str]]:
    """
    Find occurrences of terms in a piece of text. Returns all occurrences
    of each matched term with a margin around the term for offspring concept
    selection.

    Parameters
    ----------
    text_string : str
        The text in which to search for terms.
    term_to_id : Dict[str, str]
        Map between terms and their IDs. Terms should be normalized to the same
        format as `text_string` for simple match and margin slicing.
    match_method : Callable[[str, str], bool]
        Function called on (`text`, `term`) that returns whether `text` is a
        match for `term`. In the most naive application, `match_method` can be
        `map_modifiers.match.match_simple`, which checks if `term` is a
        substring of `text`. (Since no other arguments can be passed here,
        consider using `functools.partial` to pre-pass arguments to a function)
    margin_method : Callable[[str, str], List[str]]
        Function called on (`text`, `term`) that returns a list of `term`
        occurrences in `text`, including some margin around `text`.

    Returns
    -------
    List[Dict[str, str]]
        List of dictionaries representing occurrences of matched terms. Terms
        appearing multiple times in `text_string` will result in multiple list
        items.
    """
    matched_terms = [
        term for term in term_to_id.keys()
        if match_method(text_string, term)
    ]

    matches = list()
    for term in matched_terms:
        substrings = margin_method(text_string, term)
        new_matches = [
            {
                "matched_term": term,
                "ID": term_to_id[term],
                "margin": substring
            }
            for substring in substrings
        ]
        matches.extend(new_matches)
    return matches


def match_simple(string: str, term: str) -> bool:
    return term in string


def match_levenshtein(string: str, term: str, threshold: int) -> bool:
    distance = map_modifiers.similarity.levenshtein_distance(string, term)
    return distance < threshold


def slice_character_margin(string: str, term: str, margin: int) -> List[str]:
    """Slice by characters around the matched synonym"""
    slices = list()
    for match in re.finditer(pattern=term, string=string):
        start_index = match.start()
        slices.append(
            string[max(start_index - margin, 0):start_index + margin]
        )
    return slices


def slice_word_margin(string: str, term: str, margin: int) -> List[str]:
    """Slice by words around occurrences of a matched word."""
    search_string = re.compile(
        # pick up`margin` number of words before `word`
        r'([^ ]+\ ){,' + str(margin) + r'}'
        # `word` and everything between it and whitespace
        # eg. match 'b' from 'abc' -> 'abc'
        r'([^ ]*' + term + r'[^ ]*)'
        # pick up `margin` number of words after `word`
        r'(\ [^ ]+){,' + str(margin) + r'}'
    )
    slice_matches = re.finditer(search_string, string)
    return [match.group(0) for match in slice_matches]
