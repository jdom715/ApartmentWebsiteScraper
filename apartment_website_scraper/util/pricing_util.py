# coding=utf-8
"""
Utility functions related to pricing tags on the property page
"""
import re


def normalize_pricing_contents(pricing_contents: str) -> int:
    normalized_pricing_contents: str = re.sub("[$|,]", "", pricing_contents)
    pricing: int = int(normalized_pricing_contents)
    return pricing
