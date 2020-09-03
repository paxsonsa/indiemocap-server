# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" session.py

Messaging Tools for Session Updates

Author: Andrew Paxson
"""
from indiemocap import messaging
from indiemocap import message_types


class SessionInitMessage(messaging.Message):

    mtype = message_types.SessionInit

    def __init__(self, client_name, host_port, is_video_supported, major_version, minor_version, patch_version):
        self.client_name = client_name
        self.host_port = host_port
        self.is_video_supported = is_video_supported
        self.verison = (major_version, minor_version, patch_version,)


class SessionInitMessageHandler(messaging.MessageHandler):

    mtype = message_types.SessionInit
    messageKlass = SessionInitMessage

    # The byte structure for the 'struct' module
    #  1 bytes bool
    #  3 bytes padding (not used as data)
    # 32 bytes for unicode8 string
    #  4 bytes unsigned int
    #  4 bytes unsigned int
    #  4 bytes unsigned int
    byte_structure = '?3c32sIII'
    name_byte_mapping = [
        "is_video_supported",
        None, None, None,
        "client_name",
        "major_version",
        "minor_version",
        "patch_version",
    ]

    decode_hooks = {
        "client_name": messaging.decode_unicode
    }

    metadata_keys = [
        "host_port"
    ]
