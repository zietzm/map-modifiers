import re


def normalize(string: str) -> str:
    """
    Processess string to remove all non-alphabet characters and replaces all
    other delimiters (eg. newlines, multiple spaces, tabs) with single spaces.
    """
    # Make lowercase, replace natural delimiters with spaces
    s = string.lower().replace('\n', ' ').replace('\t', ' ')

    # Remove characters other than the alphabet and spaces (filling with space)
    s = re.sub(pattern=r'[^a-z\s]+', repl=' ', string=s, count=0)

    # Convert multiple spaces into single spaces
    s = re.sub(pattern=r'\s+', repl=' ', string=s, count=0)
    return s.strip()
