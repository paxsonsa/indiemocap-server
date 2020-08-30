# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" errors.py
Error Codes

Author: Andrew Paxson
"""
from indiemocap import messaging
from indiemocap import message_types


class ErrorMessage(messaging.MessageEncoder):

    mtype = message_types.Error

    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message

    def encode_body(self):
        error_code = messaging.safe_pack_message('i', self.error_code)
        encoded_str = self.message.encode('utf-16')
        return error_code + encoded_str
