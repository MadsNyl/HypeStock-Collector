def is_string_valid(string: str) -> bool:
    """
        Checks if string is a valid ticker candidate.
    """
    return 5 >= len(string) >= 2 and string[0].isupper() and string[len(string) - 1].isupper()
