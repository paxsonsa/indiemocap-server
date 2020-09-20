# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" echo.py
Module containing the EchoSessionDelegate

Author: Andrew Paxson
"""
from . import BaseSessionDelegate


class EchoSessionDelegate(BaseSessionDelegate):

    def get_session_name(self):
        return super(self).get_session_name() + " echo"

    def session_did_initialize(self, client_info):
        print("Session Did Initialize: {0}".format(client_info))

    def session_did_shutdown(self):
        print("Session Did Shutdown")

    def session_did_reset(self):
        print("Session Did Reset")

    def mode_did_change(self, mode):
        print("Session Mode Did Change to: {0}".format(mode))

    def did_recieve_motion_data(self, motion_data):
        print("Session Did Process Motion Data: {0}".format(motion_data))
