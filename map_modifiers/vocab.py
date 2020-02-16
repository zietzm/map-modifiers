import json
import lzma
from typing import Dict, List, Set, Union


def load_compressed_json_vocabulary(file_path) -> Dict[str, Union[str, List]]:
    """
    Load vocabulary file from disk.

    `map-modifiers` used three vocabulary files for rapid search and mapping.
    These are `parent_terms`, `parent_to_candidates`, and `candidate_to_id`.
    Though LZMA compression does increase the time it takes to load a
    vocabulary from disk (though time is typically the same order of magnitude)
    these operations will be performed only once. LZMA compression offers huge
    disk space savings, which is important for Python packaging.
    """
    with lzma.open(file_path, 'r') as f:
        return json.load(f)


def prune_term_list(terms: List[str]) -> Set[str]:
    """
    Removes strings from a list where substrings are present.

    Should be called on the terms for every concept when building the
    vocabulary used to search a criteria string.

    Examples
    --------
    >>> prune_term_list(['abc', 'abcd', 'abcde'])
    {'abc'}
    >>> prune_term_list(['ab', 'abc', 'de', 'def'])
    {'ab', 'de'}
    >>> prune_term_list(['ab', 'abc', 'bc'])
    {'ab', 'bc'}
    """
    sorted_terms = sorted(terms, key=len, reverse=False)
    subs = set()
    while sorted_terms:
        term = sorted_terms.pop(-1)
        subbed = False
        for item in sorted_terms:
            if item in term:
                subbed = True
                break
        if not subbed:
            subs.add(term)
    return subs
