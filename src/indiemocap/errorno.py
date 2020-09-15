# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" errorno.py
Error Numbers

Author: Andrew Paxson
"""
ERROR_BAD_MTYPE = 10
ERROR_BAD_HANDSHAKE = 11

ERROR_SESSION_INIT_FAILED = 20


class SessionErrorException(Exception):
    """ Generic Error for Sessions that can be sent over the wire """
    def __init__(self, errorno, msg):
        self.session_errorno = errorno
        super(SessionErrorException, self).__init__(msg)


def make_session_error(errorno, message):
    """ Returns a SessionErrorException """
    return SessionErrorException(errorno, message)
