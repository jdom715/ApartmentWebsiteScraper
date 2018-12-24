# coding=utf-8
"""
Utility functions related to pricing tags on the property page
"""
import re

from bs4 import Tag

PRICING_CLASS: str = "pricing"


def get_pricing_from_tag(tag: Tag) -> int:
    pricing_contents: str = tag.get_text()
    return _normalize_pricing_contents(pricing_contents)


def _normalize_pricing_contents(pricing_contents: str) -> int:
    normalized_pricing_contents: str = re.sub("[$|,]", "", pricing_contents)
    pricing: int = int(normalized_pricing_contents)
    return pricing


def is_pricing_class(class_) -> bool:
    return class_ is not None and re.compile(PRICING_CLASS).search(class_) is not None


def is_not_pricing_class(class_) -> bool:
    return not is_pricing_class(class_)
