# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" handshakes.py

Author: Andrew Paxson
"""
from indiemocap import message_types
from indiemocap.messages import (
    MessageEncoder,
    MessageHandler,
    safe_pack_message,
    safe_unpack_message,
)

class HandshakeMessage(MessageEncoder):

    mtype = message_types.Handshake

    def __init__(self, version, host_port):
        self.verison_str = version
        self.host_port = host_port

    def encode_body(self):
        major, minor, patch = self.verison_str.split(".")
        body = safe_pack_message("iii", int(major), int(minor), int(patch))
        return body


class HandshakeHandler(MessageHandler):

    mtype = message_types.Handshake

    def process(self, transport, metadata, data):
        unpacked_data = safe_unpack_message('iii', data)
        if unpacked_data is None:
            # TODO Send Error
            return
        return HandshakeMessage(".".join([str(num) for num in unpacked_data]), metadata.get("host_port"))

        # TODO Check Supported Versions

        # header = messages.safe_pack_header(message_types.Handshake)
        # message = messages.safe_pack_message('iii', 1, 0, 0)
        # messages.send_message(sock, metadata.get_key("host_port"), header, message)
