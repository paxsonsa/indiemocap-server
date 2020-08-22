# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" messages.py
Functions for decoding and encode messages

Author: Andrew Paxson
"""
import logging
import struct


def safe_unpack_header(data):
    # Incomplete message
    if len(data) < 4:
        return

    # Obtain Message Header
    header = data[:4]
    message_type = struct.unpack('i', header)[0]

    return dict(
        mtype=message_type
    )


def safe_unpack_message(fmt, data):
    try:
        message_body = struct.unpack(fmt, data)
    except struct.error as error:
        logging.error(error)
        return None
    else:
        return message_body


def safe_pack_header(mtype):
    return struct.pack('i', mtype)


def safe_pack_message(fmt, *values):
    return struct.pack(fmt, *values)


def send_message(sock, hostname, header, message):
    sock.sendto(header + message, hostname)


class MessageEncoder:

    mtype = None

    def encode(self):
        return self.encode_header() + self.encode_body()

    def encode_header(self):
        return struct.pack('i', self.mtype)

    def encode_body(self):
        raise NotImplementedError


class MessageHandler:

    def process(self, transport, metadata, data):
        raise NotImplementedError
