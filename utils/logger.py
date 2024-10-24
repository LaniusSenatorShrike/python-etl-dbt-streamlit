"""
logger.py: A module providing logging configuration
and utility functions to set up and manager logger for python applications
"""

import logging
import os
import sys


def setup_logging():
    """
    configure the logging setting
    """

    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(module)s - %(levelname)s: %(message)s", stream=sys.stdout
    )


def get_logger(name):
    return logging.getLogger(name)
