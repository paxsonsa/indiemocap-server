# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" base.py
Module containing BaseSessionDelegate class

Author: Andrew Paxson
"""
import socket


class BaseSessionDelegate:
    """ A base class for a session delegate"""

    def get_session_name(self):
        """ Returns the session name (defaults to hostname)
        Returns:
            str
        """
        return socket.gethostname()

    def session_did_initialize(self, client_info):
        raise NotImplementedError()

    def session_did_shutdown(self):
        raise NotImplementedError()

    def session_did_reset(self):
        raise NotImplementedError()

    def mode_did_change(self, mode):
        raise NotImplementedError()

    def did_recieve_motion_data(self, motion_data):
        raise NotImplementedError()
