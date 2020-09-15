# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" transport.py
Protocol Transport

Author: Andrew Paxson
"""
import indiemocap.log

from indiemocap import messaging
from indiemocap import errorno
from indiemocap.messages import errors

LOG = indiemocap.log.get_logger()

class ProtocolTransport:

    def __init__(self):
        self.connection = None
        self.registered_handlers = {}

    def handled_recieved(self, data, metadata):
        # Returns message, error
        # Incomplete message
        if len(data) < 4:
            return None, None

        header = messaging.safe_unpack_header(data)
        message_processor = self.registered_handlers.get(header['mtype'])

        if message_processor:
            return message_processor.process(self, metadata, data[messaging.MESAGE_HEADER_SIZE:]), None
        else:
            LOG.error("Error Occurred: no message process for mtype '{0}'".format(header["mtype"]))
            error_msg = errors.ErrorMessage(errorno.ERROR_BAD_MTYPE, "Cannot process message type.")
            return None, error_msg

    def handle_send(self, message, metadata):
        return message.encode()

    def register_handlers(self, handlers):
        for handler in handlers:
            print(handler.mtype)
            self.registered_handlers[handler.mtype] = handler
