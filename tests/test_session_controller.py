# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" test_session_controller.py
 Test Suite for the SessionController Class

Author: Andrew Paxson
"""
import mock
import unittest

from indiemocap.session import Session
from indiemocap.session_controller import SessionController
from indiemocap.message_types import SessionStarted, Error
from indiemocap.errorno import make_session_error, ERROR_SESSION_INIT_FAILED

DEFAULT_SERVER_NAME = "ServerName"
FAKE_CLIENT = {"hello": "value"}


class TestSessionController(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.session.supports_video = False

        self.delegate_mock = mock.Mock()
        self.delegate_mock.get_session_name.return_value = DEFAULT_SERVER_NAME

        self.test_controller = SessionController(self.session,
                                                 self.delegate_mock)

    def test_session_configured_with_client_info(self):
        self.test_controller.initialize_session(FAKE_CLIENT)
        assert self.session.client_info == FAKE_CLIENT, (
            "Expected client_info to be set"
        )

    def test_controller_delegate_called_when_initialized(self):
        self.test_controller.initialize_session(FAKE_CLIENT)
        assert self.delegate_mock.session_did_reset.called
        assert self.delegate_mock.get_session_name.called
        assert self.delegate_mock.session_did_initialize.called

    def test_response_is_success(self):
        response = self.test_controller.initialize_session(FAKE_CLIENT)
        assert response.mtype == SessionStarted
        assert not response.is_video_supported
        assert response.server_name == DEFAULT_SERVER_NAME

    def test_response_is_error(self):
        func = make_session_error(ERROR_SESSION_INIT_FAILED, "Some Error")
        self.delegate_mock.session_did_initialize.side_effect = func

        response = self.test_controller.initialize_session(FAKE_CLIENT)
        assert response.mtype == Error
        assert response.error_code == ERROR_SESSION_INIT_FAILED
        assert response.message == "Some Error"

    def test_controller_reset(self):
        self.test_controller.initialize_session(FAKE_CLIENT)
        self.test_controller.update_mode(Session.modes.Record)
        assert self.session.client_info == FAKE_CLIENT
        assert self.session.mode == Session.modes.Record

        self.test_controller.reset_session()
        assert self.session.client_info is None
        assert self.session.mode == Session.modes.Stopped
