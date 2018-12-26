# coding=utf-8
import logging
import sys


def initialize_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def log_and_exit(msg: str):
    logging.fatal(msg)
    sys.exit(1)
