# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" session_manager.py
Session Manager Class

Author: Andrew Paxson
"""
from indiemocap import responses

class SessionController:
    def __init__(self, delegate=None):
        self.client_info = None
        self.delegate = delegate
        self.state = {
            "mode": 0
        }

    def initialize_session(self, client_info):
        name = "My Server"
        self.state["client_info"] = client_info

        if self.delegate:
            name = self.delegate.get_session_name() or name
            # TODO Error
            print("Starting Init")
            self.delegate.session_did_initialize(client_info)

        return responses.SessionStartedResponse(
            name,
            is_video_supported=False
        )

    def update_mode(self, mode):
        self.state["mode"] = mode
        if self.delegate:
            # TODO Handle Errors
            self.delegate.mode_did_change(mode)

    def process_motion_data(self, motion_data):
        # TODO check mode
        print(motion_data)
        if self.delegate:
            # TODO Handle Error/Response
            self.delegate.did_recieve_motion_data(motion_data)
        return None

    def make_heartbeat(self):
        return responses.SessionHeartbeatResponse()
