from hashlib import sha1
from json import dumps

from truckersmp.cache import Cache
from typing import Callable

INVISIBLE_CHAR = "ㅤ"


def trim_string(string: str, max_chars: int = 8, add_dots: bool = True):
    """Trims a string to a set length and adds ... to the string"""
    if len(string) > max_chars:
        string = string[:max_chars]
        if add_dots:
            string += "..."
    return string


def strip_dict_key_value(dictionaries: list, key: str):
    """Strip the value from a dictionary using a key in a list of dictionaries"""
    values = list()
    for dictionary in dictionaries:
        values.append(dictionary[key])
    return values
