# coding=utf-8
"""
Util for generating reports for a given set of apartment information.
"""
import logging
from typing import Dict, List

from model.apartment_info import ApartmentInfo
from model.property_info import PropertyInfo
from util import logging_util
from util.logging_util import Level


def generate_property_summary_report(apt_info: Dict[PropertyInfo, List[ApartmentInfo]]):
    logging.info("================================GENERATING PROPERTIES SUMMARY REPORT================================")
    for property_info, apartments in apt_info.items():
        logging_util.log_property_info(msg_prefix="Found {0} apartments".format(len(apartments)),
                                       property_info=property_info,
                                       level=Level.Info)
