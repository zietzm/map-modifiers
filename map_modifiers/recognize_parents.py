import re


def get_character_margin(text, synonym, margin):
    """Slice by characters around the matched synonym"""
    slices = list()
    for match in re.finditer(synonym, text):
        start_index = match.start()
        slices.append(
            text[max(start_index - margin, 0):start_index + margin]
        )
    return slices


def get_word_margin(text, synonym, margin):
    """Slice by words around the matched synonym"""
    search_string = re.compile(
        # pick up`margin` number of words before synonym
        r'([^ ]+\ ){,' + str(margin) + r'}'
        # synonym and everything between it and whitespace
        # eg. match 'b' from 'abc' -> 'abc'
        r'([^ ]*' + synonym + r'[^ ]*)'
        # pick up `margin` number of words after synonym
        r'(\ [^ ]+){,' + str(margin) + r'}'
    )
    slice_matches = re.finditer(search_string, text)
    return [match.group(0) for match in slice_matches]


def find_possible_pre_coordination(text, synonym_to_code, word_margin):
    """
    Find all concepts with synonyms that appear in the text

    Parameters
    ----------
    text : str
        Text in which to match synonyms. Typically the text first should be
        normalized using `utils.normalize_text` to maximize the chance of a
        successful match.
    synonym_to_code : Dict[str, *]
        Dictionary mapping concept synonyms to concept codes. Typically the
        synonmys will also have been normalized using `utils.normalize_text`.
        This can be a many-to-one mapping.
    word_margin : int
        Number of words (space delimited character groups) on either side of a
        match to include in slices.

    Returns
    -------
    List[Dict[str, *]]
        List of matches within the text. `'criteria_string'` is a slice of the
        original text around a match.
    """
    matched_synonyms = [
        name for name in synonym_to_code if name in text
    ]

    all_matches = list()
    for matched_synonym in matched_synonyms:
        slices = get_word_margin(text, matched_synonym, word_margin)
        all_matches.extend([
            {
                'parent_code': synonym_to_code[matched_synonym],
                'matched_synonym': matched_synonym,
                'criteria_string': text_slice
            }
            for text_slice in slices
        ])
    return all_matches
