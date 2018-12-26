# coding=utf-8
"""
Main scraper for Capitol Hill Equity Apartments
"""
import logging
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Set, Tuple

from apartment_website_scraper.model.apartment_info import ApartmentInfo
from apartment_website_scraper.model.property_info import PropertyInfo
from apartment_website_scraper.scrapers.equity_apartments import neighborhood_website_scraper
from apartment_website_scraper.scrapers.equity_apartments import property_website_scraper
from apartment_website_scraper.scrapers.equity_apartments.constants import EXPECTED_CAPITOL_HILL_PROPERTIES, \
    CAPITOL_HILL_EQUITY_APARTMENTS_URL
from apartment_website_scraper.util import report_util
from common.util import logging_util


def main():
    start: float = time.monotonic()
    logging_util.initialize_logger()

    properties: Set[PropertyInfo] = _get_capitol_hill_properties()

    e: ThreadPoolExecutor = ThreadPoolExecutor(len(properties))
    properties_with_complete_info: Dict[PropertyInfo, List[ApartmentInfo]] = dict(
        e.map(_get_apartments_with_complete_information, properties))

    end: float = time.monotonic()
    logging.debug("Script took %s seconds to execute before generating reports.", end - start)
    report_util.generate_property_summary_report(properties_with_complete_info)


def _get_apartments_with_complete_information(property_info: PropertyInfo) -> Tuple[
    PropertyInfo, List[ApartmentInfo]]:
    property_apts: List[ApartmentInfo] = property_website_scraper.get_apartments_with_complete_information(
        property_info=property_info)
    return property_info, property_apts


def _get_capitol_hill_properties() -> Set[PropertyInfo]:
    properties: Set[PropertyInfo] = neighborhood_website_scraper.get_properties(
        CAPITOL_HILL_EQUITY_APARTMENTS_URL)
    if len(properties) != EXPECTED_CAPITOL_HILL_PROPERTIES:
        logging_util.log_and_exit(
            "Found an unexpected amount of apartment URLs: {0}".format(len(properties)))
    else:
        return properties


if __name__ == "__main__":
    main()
