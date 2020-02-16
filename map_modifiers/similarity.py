def levenshtein_distance(string_a: str, string_b: str) -> int:
    """
    Computes a string similarity metric called the Levenshtein or edit distance

    Modified from TheAlgorithms for Python.

      https://github.com/TheAlgorithms/Python/blob/
      4866b1330bc7c77c0ed0e050e6b99efdeb026448/strings/
      levenshtein_distance.py#L16-L64

    TheAlgorithms implementation was released under the MIT License,
    (reproduced below).

    Copyright (c) 2019 The Algorithms
    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
     FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
     DEALINGS IN THE SOFTWARE.

    Parameters
    ----------
    string_a : str
    string_b : str

    Returns
    -------
    int
        The Levenshtein distance between the two strings

    Examples
    --------
    >>> levenshtein_distance("planet", "planetary")
    3
    >>> levenshtein_distance("", "test")
    4
    >>> levenshtein_distance("book", "back")
    2
    >>> levenshtein_distance("book", "book")
    0
    >>> levenshtein_distance("test", "")
    4
    >>> levenshtein_distance("", "")
    0
    >>> levenshtein_distance("orchestration", "container")
    10
    """
    # The longer word should come first
    if len(string_a) < len(string_b):
        return levenshtein_distance(string_b, string_a)

    if len(string_b) == 0:
        return len(string_a)

    previous_row = range(len(string_b) + 1)

    for i, c1 in enumerate(string_a):
        current_row = [i + 1]
        for j, c2 in enumerate(string_b):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)

            # Only use the best path to each location
            current_row.append(min(insertions, deletions, substitutions))
        # Store row and move to next row
        previous_row = current_row
    # Returns the last element (distance)
    return previous_row[-1]
