# coding=utf-8
"""
Scraper for processing a specific property's apartments
"""
import re
from typing import List, Optional

from
from bs4 import Tag, BeautifulSoup

from model.apartment_info import ApartmentInfo
from model.property_info import PropertyInfo
from scrapers.equity_apartments.class_constants import LIST_GROUP_ITEM_CLASS, UNAVAILABLE_TEXT_CLASS
from util import pricing_util, square_footage_util
from util.logging_util import Level, log_property_info
from util.tag_constants import SPAN


def get_apartments_with_complete_information(property_info: PropertyInfo) -> List[ApartmentInfo]:
    unit_list_items = _get_unit_list_items(property_info)

    apts_with_complete_info = [_get_apartment_from_unit_list_item(i, property_info, unit) for i, unit in
                               enumerate(unit_list_items) if
                               _get_apartment_from_unit_list_item(i, property_info, unit) is not None]

    return apts_with_complete_info


def _get_apartment_from_unit_list_item(i: int, property_info: PropertyInfo, unit: Tag):
    if _unit_is_not_available(unit):
        log_property_info(msg_prefix="Unit {0} is unavailable".format(i),
                          property_info=property_info, level=Level.Debug)
        return None
    else:
        return _get_apartment_with_complete_info(property_info, i, unit)


def _get_unit_list_items(property_info: PropertyInfo) -> List[Tag]:
    property_url: str = property_info.get_property_url()
    apt_src: BeautifulSoup = beautiful_soup_util.get_source_from_url(property_url)
    unit_list_items: List[Tag] = apt_src.find_all(class_=re.compile(LIST_GROUP_ITEM_CLASS))
    if not unit_list_items:
        log_property_info(msg_prefix="Could not find unit list items",
                          property_info=property_info,
                          level=Level.Fatal)
    return unit_list_items


def _get_apartment_with_complete_info(property_info: PropertyInfo, i: int, unit: Tag) -> Optional[ApartmentInfo]:
    pricing_tag: Tag = _get_pricing_tag(i, property_info, unit)
    pricing: int = _get_pricing(i, property_info, pricing_tag)
    sq_ft: int = _get_square_footage(i, property_info, unit)
    apt: ApartmentInfo = ApartmentInfo(property_info=property_info, pricing=pricing,
                                       square_footage=sq_ft)
    return apt


def _get_pricing_tag(i: int, property_info: PropertyInfo, unit: Tag) -> Tag:
    pricing_tag: Tag = unit.find(class_=pricing_util.is_pricing_class)
    if pricing_tag is None:
        log_property_info(msg_prefix="Could not find pricing tag for unit {0}".format(i),
                          property_info=property_info, level=Level.Fatal)
    return pricing_tag


def _get_pricing(i: int, property_info: PropertyInfo, pricing_tag: Tag) -> int:
    pricing: int = pricing_util.get_pricing_from_tag(pricing_tag)
    if pricing is None:
        log_property_info(msg_prefix="Could not get pricing from tag for unit {0}".format(i),
                          property_info=property_info,
                          level=Level.Fatal)
    return pricing


def _get_square_footage(i: int, property_info: PropertyInfo, unit: Tag):
    potential_square_feet_tags = unit.find_all(SPAN, pricing_util.is_not_pricing_class)
    sq_feet: Optional[int] = square_footage_util.get_square_footage_from_tags(potential_square_feet_tags)
    if sq_feet is None:
        log_property_info(
            msg_prefix="Could not find exact square footage for unit {0}".format(i),
            property_info=property_info, level=Level.Fatal)
    return sq_feet


def _unit_is_not_available(unit: Tag) -> bool:
    return unit.find(class_=UNAVAILABLE_TEXT_CLASS) is not None
