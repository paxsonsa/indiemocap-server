# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" transport.py
Protocol Transport

Author: Andrew Paxson
"""
from indiemocap.messages import (
    safe_unpack_header
)

from indiemocap import errors


class ProtocolTransport:

    def __init__(self):
        self.connection = None
        self.registered_handlers = {}

    def handled_recieved(self, data, metadata):
        # Incomplete message
        if len(data) < 4:
            return

        header = safe_unpack_header(data)
        message_processor = self.registered_handlers.get(header['mtype'])

        if message_processor:
            return message_processor.process(self, metadata, data[4:])
        else:
            error_msg = errors.ErrorMessage(errors.ERROR_BAD_MTYPE, "Cannot process message type.")
            self.connection.send_message(error_msg)

    def handle_send(self, message, metadata):
        return message.encode()

    def register_handlers(self, handlers):
        for handler in handlers:
            self.registered_handlers[handler.mtype] = handler
