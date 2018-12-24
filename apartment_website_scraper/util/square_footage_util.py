# coding=utf-8
import re
from typing import Optional, List, Set

from bs4 import Tag

_IS_DIGIT_REGEX: str = "[^0-9]"
_EMPTY_STRING: str = ""
_SINGLETON_SET: int = 1


def get_square_footage_from_tags(square_feet_tags: List[Tag]) -> Optional[int]:
    """
    :param square_feet_tags: Tags to search through to find square footage.
    :return: Square footage int if single tag is found, None otherwise.
    """
    sq_ft_set: Set[int] = set()
    for tag in square_feet_tags:
        sq_ft_contents: str = tag.get_text()
        sq_ft_numeric_contents: str = re.sub(_IS_DIGIT_REGEX, _EMPTY_STRING, sq_ft_contents)
        if len(sq_ft_numeric_contents) == 3:
            sq_ft_set.add(int(sq_ft_numeric_contents))
    if len(sq_ft_set) == _SINGLETON_SET:
        return sq_ft_set.pop()
    else:
        return None
