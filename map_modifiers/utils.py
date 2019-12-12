def normalize_text(text):
    """
    Normalize text to remove newlines, excessive spaces, and common characters
    that appear in eligibility criteria strings.
    """
    normalized = (
        text
        .lower()
        .replace('\n', '')
        .replace('\'', '')
        .replace('"', '')
        .replace('.', '')
        .replace(',', '')
        .replace(':', '')
        .replace(';', '')
        .replace('(', '')
        .replace(')', '')
        .replace('[x]', '')
    )
    # Remove any more than one space in a row
    while '  ' in normalized:
        normalized = normalized.replace('  ', ' ')
    return normalized
