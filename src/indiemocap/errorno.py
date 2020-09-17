# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" errorno.py
Error Numbers

Author: Andrew Paxson
"""
from indiemocap import responses


ERROR_BAD_MTYPE = 10
ERROR_BAD_HANDSHAKE = 11

ERROR_HEARTBEAT_FAILED = 20

ERROR_SESSION_INIT_FAILED = 30
ERROR_SESSION_RESET_FAILED = 31
ERROR_SESSION_MODE_CHANGE_FAILED = 32
ERROR_SESSION_MOTION_FAILED = 32


class SessionErrorException(Exception):
    """ Generic Error for Sessions that can be sent over the wire """
    def __init__(self, errorno, msg):
        self.session_errorno = errorno
        super(SessionErrorException, self).__init__(msg)


def make_session_error(errorno, message):
    """ Returns a SessionErrorException """
    return SessionErrorException(errorno, message)


def catch_error_responses(error_code, message="Unknown errored occured on server."):
    def decorator(func):
        def wrapper(*args, **kwargs):
            response = None
            try:
                response = func(*args, **kwargs)
            except SessionErrorException as err:
                response = responses.ErrorResponse(
                    err.session_errorno,
                    str(err)
                )
            except Exception as err:
                # TODO Error Logging
                response = responses.ErrorResponse(
                    error_code,
                    message
                )
            return response
        return wrapper
    return decorator
