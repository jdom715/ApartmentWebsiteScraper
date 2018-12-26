# coding=utf-8
import logging
import smtplib
import sys
import time
import traceback
from concurrent.futures.thread import ThreadPoolExecutor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

from common.util import logging_util, firefox_util
# set up the SMTP server
from nordstrom_website_scraper.model.product import Product
from nordstrom_website_scraper.model.style_type import StyleType
from nordstrom_website_scraper.repo import product_requests_repo

_PRODUCT_URL: str = "https://shop.nordstrom.com/s/schott-nyc-cafe-racer-oil-tanned-cowhide-leather-moto-jacket/3836744"
_SKU_UNAVAILABLE_CLASS: str = "SkuUnavailableText"
_PRODUCT_DESCRIPTION = "Schott NYC Leather Moto Jacket"
_SIZE_WANTED = "medium"
_COLOR_WANTED = "black"
EMAIL_ADDRESS_FROM = "jdom715@gmail.com"
EMAIL_ADDRESS_TO = "jdom715@gmail.com"


def main():
    start: float = time.monotonic()

    smtp: smtplib.SMTP = _validate_email_arguments_and_get_email_client()
    try:
        logging_util.initialize_logger()
        product_requests_repo.get_product_requests()
        driver: webdriver.Firefox = webdriver.Firefox(firefox_util.get_firefox_profile(),
                                                      options=firefox_util.get_firefox_options())
        driver.get(_PRODUCT_URL)

        product_wanted: Product = Product(description="", size=_SIZE_WANTED, color=_COLOR_WANTED, url=_PRODUCT_URL)
        if _product_is_available(driver=driver, product_wanted=product_wanted):
            description: str = _get_description(driver)
            product: Product = Product(description=description, size=_SIZE_WANTED, color=_COLOR_WANTED,
                                       url=_PRODUCT_URL)
            _send_available_email(smtp, product=product)
        else:
            logging.info("Style not available.")
        driver.quit()
        end: float = time.monotonic()
        logging.info("Nordstrom website scraper took %s seconds.", end - start)
    except Exception:
        traceback.print_exc()
        msg: MIMEMultipart = MIMEMultipart()  # create a message
        message = "There was an error with your Nordstrom website scraper script: {tb}".format(
            tb=traceback.format_exc())

        msg["From"] = EMAIL_ADDRESS_FROM
        msg["To"] = EMAIL_ADDRESS_TO
        msg["Subject"] = "There was an error with the Nordstrom Website Scraper app."

        msg.attach(MIMEText(message))
        smtp.send_message(msg)


def _product_is_available(driver: webdriver.Firefox, product_wanted: Product):
    return _style_is_available(driver, StyleType.SIZE, product_wanted.get_size()) and _style_is_available(driver,
                                                                                                          StyleType.COLOR,
                                                                                                          product_wanted.get_color())


def _send_available_email(smtp: smtplib.SMTP, product: Product):
    msg: MIMEMultipart = MIMEMultipart()  # create a message

    message = "Your {product_description} is available in style [{size},{color}].\n{link}".format(
        product_description=product.get_description(), size=product.get_size(), color=product.get_color(),
        link=product.get_url())

    msg["From"] = EMAIL_ADDRESS_FROM
    msg["To"] = EMAIL_ADDRESS_TO
    msg["Subject"] = "Your Product is Available"

    msg.attach(MIMEText(message))
    smtp.send_message(msg)

    del msg


def _validate_email_arguments_and_get_email_client() -> smtplib.SMTP:
    email_address: str = sys.argv[1]
    email_password: str = sys.argv[2]
    s = smtplib.SMTP(host="smtp.gmail.com", port=587)
    s.ehlo()
    s.starttls()
    s.login(email_address, email_password)
    return s


def _get_description(driver: webdriver.Firefox) -> str:
    css_selector: str = "h1[itemprop='name']"
    product_description_header: WebElement = driver.find_element_by_css_selector(css_selector)
    return product_description_header.text


def _style_is_available(driver: webdriver.Firefox, style_type: StyleType, style_value_wanted: str) -> bool:
    css_selector: str = "div[aria-label='{style_type} dropdown']".format(style_type=style_type.value)
    dropdown_list: WebElement = driver.find_element_by_css_selector(css_selector)
    dropdown_list.click()

    style_list: List[WebElement] = dropdown_list.find_elements_by_xpath(
        "//div[starts-with(@class, 'SkuFilterListItemBody')]")
    logging.info("Found %s styles", len(style_list))

    e: ThreadPoolExecutor = ThreadPoolExecutor(len(style_list))
    return any(
        e.map(lambda style: _style_value_is_available_from_list(style=style, style_value_wanted=style_value_wanted),
              style_list))


def _style_value_is_available_from_list(style: WebElement, style_value_wanted: str) -> bool:
    style_value: str = style.text.lower()
    logging.info("On style value %s", style_value)
    is_available = style_value_wanted in style_value and "not available" not in style_value
    if is_available:
        style.click()
        return True

    return False


if __name__ == "__main__":
    main()
