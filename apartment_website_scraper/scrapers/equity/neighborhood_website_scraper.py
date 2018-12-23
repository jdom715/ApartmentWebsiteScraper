from typing import List, Optional, Set

from bs4 import BeautifulSoup, Tag

from model.property_info import PropertyInfo
from scrapers.equity.constants import EQUITY_APARTMENTS_URL
from util.beautiful_soup_util import get_source_from_url
from util.tag_util import filter_child_tags_from_tags


def get_properties(neighborhood_url: str) -> Set[PropertyInfo]:
    page_src: BeautifulSoup = get_source_from_url(neighborhood_url)
    apt_link_headers: List[Tag] = page_src.find_all(itemprop="name")
    return _find_property_urls_and_names(apt_link_headers)


def _find_property_urls_and_names(apt_link_headers: List[Tag]) -> Set[PropertyInfo]:
    anchors_from_headers: List[Tag] = filter_child_tags_from_tags(apt_link_headers, "a")
    properties: Set[PropertyInfo] = set()
    for anchor in anchors_from_headers:
        property_info: Optional[PropertyInfo] = _get_property_from_anchor_tag(anchor)
        if property_info:
            properties.add(property_info)

    return properties


def _get_property_from_anchor_tag(anchor: Tag) -> Optional[PropertyInfo]:
    property_name: str = anchor.get_text()
    url_suffix_from_anchor: str = anchor["href"]
    property_url: str = EQUITY_APARTMENTS_URL + url_suffix_from_anchor
    if not property_name or not url_suffix_from_anchor:
        return None
    return PropertyInfo(property_name=property_name, property_url=property_url)
