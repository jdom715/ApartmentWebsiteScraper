# coding=utf-8
"""
Main scraper for Capitol Hill Equity Apartments
"""
import logging
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Dict, List, Set, Tuple

from model.apartment_info import ApartmentInfo
from model.command_line_arguments import CommandLineArguments
from model.property_info import PropertyInfo
from scrapers.equity_apartments import neighborhood_website_scraper
from scrapers.equity_apartments import property_website_scraper
from scrapers.equity_apartments.constants import EXPECTED_CAPITOL_HILL_PROPERTIES, CAPITOL_HILL_EQUITY_APARTMENTS_URL
from util import google_drive_util, logging_util, report_util


def main():
    cla: CommandLineArguments = _validate_and_get_command_line_arguments()
    start: float = time.monotonic()
    logging_util.initialize_logger()

    properties: Set[PropertyInfo] = _get_capitol_hill_properties()

    e: ThreadPoolExecutor = ThreadPoolExecutor(len(properties))
    properties_with_complete_info: Dict[PropertyInfo, List[ApartmentInfo]] = dict(
        e.map(_get_apartments_with_complete_information, properties))

    end: float = time.monotonic()
    logging.debug("Script took %s seconds to execute before generating reports.", end - start)
    google_drive_util.upload_apartment_info(cla.get_google_credentials_file_path())
    report_util.generate_property_summary_report(properties_with_complete_info)


def _validate_and_get_command_line_arguments() -> CommandLineArguments:
    if len(sys.argv) < 2:
        logging_util.log_and_exit("Not enough arguments were provided.")

    args: List[str] = sys.argv[1:]

    google_credentials_file_path: str = args[0]
    _validate_google_credentials_file(google_credentials_file_path)

    return CommandLineArguments(google_credentials_file_path=google_credentials_file_path)


def _validate_google_credentials_file(path: str):
    my_file = Path(path)
    if not my_file.is_file():
        logging_util.log_and_exit("Google credentials file path was invalid.")


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
