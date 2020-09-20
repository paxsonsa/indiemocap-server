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
from indiemocap.log import get_logger


LOG = get_logger()


class SessionController:
    def __init__(self, session, delegate=None):
        self.client_info = None
        self.session = session
        self.delegate = delegate

    @catch_error_responses(errorno.ERROR_SESSION_INIT_FAILED)
    def initialize_session(self, client_info):
        """ Initialize the session connection with the given client_info

        Args:
            client_info (dict): A dictionary of client information

        Returns:
            MessageEncoder or None
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

    def reset_session(self):
        """ Reset the session """
        self.session.reset()
        if self.delegate:
            self.delegate.session_did_reset()

    @catch_error_responses(errorno.ERROR_SESSION_MODE_CHANGE_FAILED)
    def update_mode(self, mode):
        """ Update the session's current mode

        Args:
            mode (int): The new mode to update to (from Session.modes)

        Returns:
            MessageEncoder or None
        """
        self.session.mode = mode
        if self.delegate:
            self.delegate.mode_did_change(mode)

    @catch_error_responses(errorno.ERROR_SESSION_MOTION_FAILED)
    def process_motion_data(self, motion_data):
        """ Process Incoming Motion Data

        Args:
            motion_data (MotionDataMessage): The motion data to process

        Returns:
            MessageEncoder or None

        """
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
        """ Create a new heartbeat response
        Returns:
            MessageEncoder
        """
        return responses.SessionHeartbeatResponse()

    @catch_error_responses(errorno.ERROR_SESSION_END_FAILED)
    def end_session(self):
        """ End the current sesssion connection
        Returns:
            MessageEncoder or None
        """
        if not self.session.client_info:
            return responses.ErrorResponse(
                errorno.ERROR_SESSION_END_FAILED,
                "Cannot end session, the is not session running"
            )
        self.reset_session()
        return responses.SessionEndedResponse()
