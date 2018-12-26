# coding=utf-8
"""
Utility functions/classes related to logging.
"""
import logging
import sys
from enum import Enum
from typing import Callable, Dict

from model.property_info import PropertyInfo


class Level(Enum):
    Info = "Info"
    Debug = "Debug"
    Warning = "Warning"
    Error = "Error"
    Fatal = "Fatal"


_level_to_logging_function: Dict[Level, Callable] = {
    Level.Info: logging.info,
    Level.Debug: logging.debug,
    Level.Warning: logging.warning,
    Level.Error: logging.error,
    Level.Fatal: logging.fatal
}


def log_property_info(msg_prefix: str, property_info: PropertyInfo, level: Level):
    property_info_msg: str = get_property_info_msg(msg_prefix=msg_prefix, property_info=property_info)
    logging_func: Callable = _level_to_logging_function[level]
    logging_func(property_info_msg)
    if level == Level.Fatal:
        sys.exit(1)


def get_property_info_msg(msg_prefix: str, property_info: PropertyInfo) -> str:
    return "{msg_prefix} for property {property_name} at url {property_url}".format(
        msg_prefix=msg_prefix, property_name=property_info.get_property_name(),
        property_url=property_info.get_property_url())
