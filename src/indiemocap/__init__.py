# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" __init__.py

Author: Andrew Paxson
"""
from indiemocap import (
    connection,
    connection_delegates,
    transport,
    errors,
    handshakes,
    message_types
)

default_handlers = [
    handshakes.HandshakeHandler(),
]

supported_versions = [
    "1.0.0"
]
