# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" session_manager.py
Session Manager Class

Author: Andrew Paxson
"""
from indiemocap import responses

class SessionController:
    def __init__(self):
        self.client_info = None

    def initialize_session(self, client_info):
        self.client_info = client_info

        return responses.SessionStartedResponse(
            "MyServer",
            is_video_supported=False
        )

    def make_heartbeat(self):
        return responses.SessionHeartbeatResponse()
