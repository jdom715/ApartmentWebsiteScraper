# coding=utf-8
"""
Scraper for processing a specific property's apartments
"""
import re
from typing import List, Optional

from bs4 import Tag, BeautifulSoup

from model.apartment_info import ApartmentInfo
from model.property_info import PropertyInfo
from util.beautiful_soup_util import get_source_from_url
from util.logging_util import Level, log_property_info
from util.pricing_util import normalize_pricing_contents


def get_apartments_with_complete_information(property_info: PropertyInfo) -> List[ApartmentInfo]:
    unit_list_items = _get_unit_list_items(property_info)

    apts_with_complete_info = [_get_apartment_from_unit_list_item(i, property_info, unit) for i, unit in
                               enumerate(unit_list_items) if
                               _get_apartment_from_unit_list_item(i, property_info, unit) is not None]

    return apts_with_complete_info


def _get_apartment_from_unit_list_item(i: int, property_info: PropertyInfo, unit: Tag):
    if unit_is_not_available(unit):
        log_property_info(msg_prefix="Unit {0} is unavailable".format(i),
                          property_info=property_info, level=Level.Debug)
        return None
    else:
        return _get_apartment_with_complete_info(property_info, i, unit)


def _get_unit_list_items(property_info: PropertyInfo) -> List[Tag]:
    property_url: str = property_info.get_property_url()
    apt_src: BeautifulSoup = get_source_from_url(property_url)
    unit_list_items: List[Tag] = apt_src.find_all(class_=re.compile("list-group-item"))
    if not unit_list_items:
        log_property_info(msg_prefix="Could not find unit list items",
                          property_info=property_info,
                          level=Level.Fatal)
    return unit_list_items


def _get_apartment_with_complete_info(property_info: PropertyInfo, i: int, unit: Tag) -> Optional[ApartmentInfo]:
    pricing_tag: Tag = unit.find(class_=_is_pricing_class)
    if pricing_tag is None:
        log_property_info(msg_prefix="Could not find pricing tag for unit {0}".format(i),
                          property_info=property_info, level=Level.Fatal)
    pricing: int = _get_pricing_from_tag(pricing_tag)
    if pricing is None:
        log_property_info(msg_prefix="Could not get pricing from tag for unit {0}".format(i),
                          property_info=property_info,
                          level=Level.Fatal)
        return None
    potential_square_feet_tags = unit.find_all("span", _is_not_pricing_class)
    sq_feet: Optional[int] = _get_square_footage_from_tags(potential_square_feet_tags)
    if sq_feet is None:
        log_property_info(
            msg_prefix="Could not find square footage for bedroom type {bedroom_type}",
            property_info=property_info, level=Level.Fatal)
        return None
    apt: ApartmentInfo = ApartmentInfo(property_info=property_info, pricing=pricing,
                                       square_footage=sq_feet)
    return apt


def unit_is_not_available(unit: Tag) -> bool:
    return unit.find(class_="unavailable-text") is not None


def _get_pricing_from_tag(tag: Tag) -> int:
    pricing_contents: str = tag.get_text()
    return normalize_pricing_contents(pricing_contents)


def _get_square_footage_from_tags(square_feet_tags: List[Tag]) -> Optional[int]:
    sq_feet: Optional[int] = None
    for tag in square_feet_tags:
        sq_ft_contents: str = tag.get_text()
        sq_ft_numeric_contents: str = re.sub("[^0-9]", "", sq_ft_contents)
        if len(sq_ft_numeric_contents) == 3:
            sq_feet = int(sq_ft_numeric_contents)
    return sq_feet


def _is_pricing_class(class_) -> bool:
    return class_ is not None and re.compile("pricing").search(class_) is not None


def _is_not_pricing_class(class_) -> bool:
    return not _is_pricing_class(class_)
