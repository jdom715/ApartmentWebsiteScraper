# coding=utf-8
"""
Utility functions related to the Beautiful Soup web-scraping library.
"""
import requests
from bs4 import BeautifulSoup
from requests import Response

from util.logging_util import log_and_exit


def get_source_from_url(url) -> BeautifulSoup:
    r: Response = requests.get(url)
    if r.status_code is not 200:
        log_and_exit(
            "Encountered status code {0} when sending a GET request to URL {1}".format(r.status_code, url))
    data: str = r.text
    return BeautifulSoup(data, "html.parser")
