# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" errors.py
Error Codes

Author: Andrew Paxson
"""
from indiemocap.message_types import (
    Error
)
from indiemocap.messages import (
    MessageEncoder,
    safe_pack_header,
    safe_pack_message,

)

ERROR_BAD_MTYPE = 10
ERROR_BAD_HANDSHAKE = 11


class ErrorMessage(MessageEncoder):

    mtype = Error

    def __init__(self, error_code, message):
        self.error_code = error_code
        self.message = message

    def encode_body(self):
        error_code = safe_pack_message('i', self.error_code)
        encoded_str = self.message.encode('utf-16')
        return error_code + encoded_str
