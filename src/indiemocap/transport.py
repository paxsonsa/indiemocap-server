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
    """ Class for transporting messages to and from a connection.

    By registering a list of MessageHandlers transport class can
    be used to process (decode/encode) messages (MessageEncoders).

    Attributes:
        registered_handlers (dict[int: MessageHandler]): A dictionary of
            messages types and functions to use for handling incoming messages
    """
    def __init__(self):
        """ Create a new transporter """
        self.registered_handlers = {}

    def handled_recieved(self, data, metadata):
        """ Handle the incoming data and return the decoded message

        Args:
            data (bytes): A stream of bytes to decode
            metadata (dict): Extra metadata about the message

        Returns:
            Message or None, Error Message or None
        """
        # Returns message, error
        # Incomplete message
        if len(data) < 4:
            return None, None

        header = messaging.safe_unpack_header(data)
        message_processor = self.registered_handlers.get(header['mtype'])

        if message_processor:
            return message_processor.process(
                self,
                metadata,
                data[messaging.MESAGE_HEADER_SIZE:]
            ), None
        else:
            LOG.error(
                "Error Occurred: no message process for mtype '{0}'".format(
                    header["mtype"])
            )
            error_msg = errors.ErrorMessage(
                errorno.ERROR_BAD_MTYPE,
                "Cannot process message type."
            )
            return None, error_msg

    def handle_send(self, message, metadata):
        """ Encode the message and return the bytes

        Args:
            message (MessageEncoder): The message to encode which should be a
                subclass of MessageEncoder
            metadata (dict): Extra metadata to use for processing the message.

        Returns:
            bytes
        """
        return message.encode()

    def register_handlers(self, handlers):
        """ Register a list of handler classes

        Args:
            handlers (list[MessageHandler]): A list of Messagehandlers
                to register
        """
        for handler in handlers:
            self.registered_handlers[handler.mtype] = handler
