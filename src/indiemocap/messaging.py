# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" messaging.py

Author: Andrew Paxson
"""
import logging
import struct

MESAGE_HEADER_SIZE = 16


class Message:

    def __repr__(self):
        attrs = ["{0}={1}".format(k, v) for k,v in self.__dict__.items()]
        attr_str = " ".join(attrs)
        return "{0}<{1}>".format(self.__class__.__name__, attr_str)

    def serialize(self):
        return self.__dict__

    def type(self):
        return self.type


class MessageEncoder:

    mtype = None
    byte_struct = None
    attributes = []
    encoding_hooks = {}

    def encode(self):

        body = self.encode_body()
        part_id = 1
        part_count = 1
        length = len(body)

        return self.encode_header(length, part_id, part_count) + body

    def encode_header(self, length, part_id, part_count):
        return struct.pack('IIII', self.mtype, length, part_count, part_id)

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
        return safe_pack_message(self.byte_structure, *values)


class MessageHandler:

    # TODO Document
    messageKlass = None
    byte_structure = None
    name_byte_mapping = []
    metadata_keys = []
    decode_hooks = {}

    def process(self, transport, metadata, data):
        unpacked_data = safe_unpack_message(self.byte_structure, data)
        if unpacked_data is None:
            # TODO Send Error
            return

        data = {}
        for i, key in enumerate(self.name_byte_mapping):
            if key is None:
                continue

            value = unpacked_data[i]

            # Process Value Hooks
            hook = self.decode_hooks.get(key)
            if hook:
                value = hook(value)
            data[key] = value

        for key in self.metadata_keys:
            data[key] = metadata.get(key)

        return self.messageKlass(**data)


def safe_unpack_header(data):
    # Incomplete message
    if len(data) < MESAGE_HEADER_SIZE:
        return

    # Obtain Message Header
    header = data[:MESAGE_HEADER_SIZE]
    message_type, length, part_count, part_id = struct.unpack('iiii', header)

    return dict(
        mtype=message_type,
        length=length,
        part_count=part_count,
        part_id=part_id
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


def decode_unicode(decodable):
    return decodable.decode('utf8')

def encode_unicode(encodable):
    return encodable.encode('utf8')
