# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" session_manager.py
Session Manager Class

Author: Andrew Paxson
"""
from indiemocap import responses
from indiemocap import errorno
from indiemocap.errorno import catch_error_responses
from indiemocap.session import Session


class SessionController:
    def __init__(self, session, delegate=None):
        self.client_info = None
        self.session = session
        self.delegate = delegate

    @catch_error_responses(errorno.ERROR_SESSION_INIT_FAILED)
    def initialize_session(self, client_info):
        """ Initialize the session with the given client_info

        Args:
            client_info (dict): A dictionary of client information

        Returns:
            MessageEncoder
        """
        response = self.reset_session()
        if response:
            return response

        # TODO name to be host name by default from config file.
        name = "My Server"
        self.session.client_info = client_info

        if not self.delegate:
            return responses.SessionStartedResponse(
                name,
                is_video_supported=self.session.supports_video
            )

        name = self.delegate.get_session_name() or name
        self.delegate.session_did_initialize(client_info)

        return responses.SessionStartedResponse(
            name,
            is_video_supported=self.session.supports_video
        )

    @catch_error_responses(errorno.ERROR_SESSION_RESET_FAILED)
    def reset_session(self):
        """ Reset the session """
        self.session.reset()
        if self.delegate:
            self.delegate.session_did_reset()

    @catch_error_responses(errorno.ERROR_SESSION_MODE_CHANGE_FAILED)
    def update_mode(self, mode):
        self.session.mode = mode
        if self.delegate:
            # TODO Handle Errors
            self.delegate.mode_did_change(mode)

    @catch_error_responses(errorno.ERROR_SESSION_MOTION_FAILED)
    def process_motion_data(self, motion_data):
        if self.session.mode == self.session.modes.Stopped:
            return responses.ErrorResponse(
                errorno.ERROR_SESSION_MOTION_FAILED,
                "Cannot process motion in 'stopped' mode."
            )

        if self.delegate:
            self.delegate.did_recieve_motion_data(motion_data)
        return None

    @catch_error_responses(errorno.ERROR_HEARTBEAT_FAILED)
    def make_heartbeat(self):
        return responses.SessionHeartbeatResponse()
