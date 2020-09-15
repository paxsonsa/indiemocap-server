# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" session_manager.py
Session Manager Class

Author: Andrew Paxson
"""
from indiemocap import responses
from indiemocap import session
from indiemocap import errorno

class SessionController:
    def __init__(self, session, delegate=None):
        self.client_info = None
        self.session = session
        self.delegate = delegate

    def initialize_session(self, client_info):
        """ Initialize the session with the given client_info

        Args:
            client_info (dict): A dictionary of client information

        Returns:
            MessageEncoder
        """
        # TODO Send Reset to Delegate and Session
        # TODO name to be host name by default
        name = "My Server"
        self.session.client_info = client_info

        if self.delegate:
            try:
                name = self.delegate.get_session_name() or name
                self.delegate.session_did_initialize(client_info)

            except errorno.SessionErrorException as err:
                return responses.ErrorResponse(
                    err.session_errorno,
                    str(err)
                )

            except Exception as err:
                # TODO Error Logging
                return responses.ErrorResponse(
                    errorno.ERROR_SESSION_INIT_FAILED,
                    "Unknown errored occured on server."
                )

        return responses.SessionStartedResponse(
            name,
            is_video_supported=self.session.supports_video
        )

    def update_mode(self, mode):
        self.session.mode = mode
        if self.delegate:
            # TODO Handle Errors
            self.delegate.mode_did_change(mode)

    def process_motion_data(self, motion_data):
        if self.session.mode == self.session.modes.Stopped:
            # TODO Handle Error/Response
            return

        print(motion_data)
        if self.delegate:
            # TODO Handle Error/Response
            self.delegate.did_recieve_motion_data(motion_data)
        return None

    def make_heartbeat(self):
        return responses.SessionHeartbeatResponse()
