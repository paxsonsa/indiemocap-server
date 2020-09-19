# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" log.py
Logging Setup

Author: Andrew Paxson
"""
import logging

LOGGER = None


def get_logger():
    logging.basicConfig(level=logging.DEBUG)

    global LOGGER
    if LOGGER is None:
        LOGGER = logging.getLogger("indiemocap-server")
    return LOGGER
