# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" heartbeat.py
Heartbeat Message and Handler

Author: Andrew Paxson
"""
from indiemocap import messaging
from indiemocap import message_types

class SessionHeartbeatMessage(messaging.Message):
    mtype = message_types.SessionHeartbeat


class SessionHeartbeatHandler(messaging.MessageHandler):

    mtype = message_types.SessionHeartbeat
    messageKlass = SessionHeartbeatMessage

    byte_structure = None
    name_byte_mapping = []

    def process(self, transport, metadata, data):
        return SessionHeartbeatMessage()

