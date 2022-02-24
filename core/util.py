
INVISIBLE_CHAR = "ㅤ"


def trim_string(string: str, max_chars: int = 8, add_dots: bool = True):
    """Trims a string to a set length and adds ... to the string"""
    if len(string) > max_chars:
        string = string[:max_chars]
        if add_dots:
            string += "..."
    return string
