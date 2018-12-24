# coding=utf-8
"""
Utility functions related to tags
"""
from typing import List

from bs4 import Tag


def filter_child_tags_from_tags(tags: List[Tag], child_tag: str) -> List[Tag]:
    """
    :param tags: List of tags to filter
    :param child_tag: String of the child tag to filter by
    :return: List of the child tags matching the child_tag input.
    """

    return [_find_child_tag(tag, child_tag) for tag in tags
            if _find_child_tag(tag, child_tag) is not None]


def _find_child_tag(tag: Tag, child_tag_to_find: str) -> Tag:
    return tag.find(child_tag_to_find)
