# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" responses.py
Responses for the client

Author: Andrew Paxson
"""
from indiemocap import messaging
from indiemocap import messages
from indiemocap import message_types


class ErrorResponse(messaging.MessageEncoder):

    mtype = message_types.Error

    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message

    def encode_body(self):
        error_code = messaging.safe_pack_message('i', self.error_code)
        encoded_str = self.message.encode('utf-16')
        return error_code + encoded_str


class SessionStartedResponse(messaging.Message, messaging.MessageEncoder):
    # TODO Add Validation
    mtype = message_types.SessionStarted
    byte_structure = '32s?'
    attributes = [
        "server_name",
        "is_video_supported"
    ]

    encoding_hooks = {
        "server_name": messaging.encode_unicode
    }

    def __init__(self, server_name, is_video_supported):
        self.server_name = server_name
        self.is_video_supported = is_video_supported

    def encode_body(self):
        values = []
        for attr in self.attributes:
            value = getattr(self, attr)
            if self.encoding_hooks.get(attr):
                value = self.encoding_hooks.get(attr)(value)
            values.append(
                value
            )
        return messaging.safe_pack_message(self.byte_structure, *values)


class SessionHeartbeatResponse(messaging.Message, messaging.MessageEncoder):

    mtype = message_types.SessionHeartbeat
    byte_struct = None

    def encode_body(self):

        if not self.byte_struct:
            return b''

        values = []
        for attr in self.attributes:
            value = getattr(self, attr)
            if self.encoding_hooks.get(attr):
                value = self.encoding_hooks.get(attr)(value)
            values.append(
                value
            )
        return messaging.safe_pack_message(self.byte_structure, *values)
