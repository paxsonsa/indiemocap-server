# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" motion_data.py
MotionData Message Handler

Author: Andrew Paxson
"""
from indiemocap import messaging
from indiemocap import message_types


class ModeChangedMessage(messaging.Message):

    mtype = message_types.SessionModeChanged

    def __init__(self, newMode):
        self.mode = newMode


class ModeChangedHandler(messaging.MessageHandler):

    mtype = message_types.SessionModeChanged
    messageKlass = ModeChangedMessage


    # Integer Representing New Mode
    byte_structure = 'I'
    name_byte_mapping = [
        "newMode"
    ]
