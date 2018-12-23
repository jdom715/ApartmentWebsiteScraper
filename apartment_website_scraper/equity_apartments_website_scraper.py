# coding=utf-8
"""
Main scraper for Capitol Hill Equity Apartments
"""
import logging
import time
from typing import Dict, List, Set

from model.apartment_info import ApartmentInfo
from model.property_info import PropertyInfo
from scrapers.equity import neighborhood_website_scraper
from scrapers.equity import property_website_scraper
from scrapers.equity.constants import EXPECTED_CAPITOL_HILL_PROPERTIES, CAPITOL_HILL_EQUITY_APARTMENTS_URL
from util import logging_util, report_util


def main():
    start: float = time.monotonic()
    logging_util.initialize_logger()

    properties_with_complete_info: Dict[PropertyInfo, List[ApartmentInfo]] = {}
    properties: Set[PropertyInfo] = _get_capitol_hill_properties()
    for property_info in properties:
        property_apts: List[ApartmentInfo] = property_website_scraper.get_apartments_with_complete_information(
            property_info=property_info)
        properties_with_complete_info[property_info] = property_apts

    end: float = time.monotonic()
    logging.debug("Script took %s seconds to execute before generating reports.", end - start)
    report_util.generate_property_summary_report(properties_with_complete_info)


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
