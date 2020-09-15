# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" __init__.py

Author: Andrew Paxson
"""
from indiemocap import (
    connection,
    connection_delegates,
    session_delegates,
    messages,
    transport,
    session_controller,
    session,
    server,
)

default_handlers = [
    messages.SessionInitMessageHandler(),
    messages.SessionHeartbeatHandler(),
    messages.ModeChangedHandler(),
    messages.MotionDataHandler(),
]

supported_versions = [
    "1.0.0"
]
