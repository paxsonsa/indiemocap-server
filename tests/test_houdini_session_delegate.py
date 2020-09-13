# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" test_houdini_session_delegate.py
Test Suite for the Houdini Session Delegate

Author: Andrew Paxson
"""
import mock
import struct
import time
import unittest

from mocks.session_controller import MockSessionController
from mocks.houdini_pipein import MockPipeInServer

from indiemocap.messages.motion_data import MotionDataMessage
import indiemocap.session
import indiemocap.session_delegates.houdini as houdini

P_ARGS = 0

class TestHoudiniDelegateLifeCycle(unittest.TestCase):

    def setUp(self):
        self.mock_socket = mock.Mock()
        self.delegate = houdini.HoudiniSessionControllerDelegate()
        self.delegate.socket = self.mock_socket

    def test_basic_lifecycle(self):
        """ Test the basic lifecycle of the delegate """
        msg_index = 0
        # Simulate the session initialize and the user
        # went to live mode.
        client_info = {"name": "MyServer"}
        self.delegate.session_did_initialize(client_info)

        msg = self.mock_socket.sendall.call_args_list[msg_index][P_ARGS][0]
        self.assertTrue(is_reset(msg))
        msg_index += 1

        msg = self.mock_socket.sendall.call_args_list[msg_index][P_ARGS][0]
        comannd_type, channel_count = struct.unpack_from('!qq', msg)

        self.assertEqual(comannd_type, houdini.commands.NAMES)
        # Motion Data is recorded as 6 distinct channels for rotation and position
        self.assertEqual(channel_count, 6)

        # Each channel name is sent as a series of 8 byte chunks (char*)
        # Each channel is preceeded by the number of chunks which
        # is always one for the channels names
        offset = struct.calcsize('!qq')
        offset = check_channel_name(msg, offset, "yaw", 1)
        offset = check_channel_name(msg, offset, "pitch", 1)
        offset = check_channel_name(msg, offset, "roll", 1)
        offset = check_channel_name(msg, offset, "accX", 1)
        offset = check_channel_name(msg, offset, "accY", 1)
        offset = check_channel_name(msg, offset, "accZ", 1)

        msg_index += 1

        # Send some motion data
        motion_data = [-1.0, 0.0, 1.0, 1.0, 2.0, 3.0]
        self.delegate.did_recieve_motion_data(
            MotionDataMessage(*motion_data)
        )

        msg = self.mock_socket.sendall.call_args_list[msg_index][P_ARGS][0]
        self.assertTrue(is_reset(msg))
        msg_index += 1


        offset = 0
        msg = self.mock_socket.sendall.call_args_list[msg_index][P_ARGS][0]
        command_type, channel_count = struct.unpack_from('!qq', msg)
        offset += struct.calcsize('!qq')
        self.assertEqual(command_type, houdini.commands.VALUE)
        self.assertEqual(channel_count, 6)

        for data in motion_data:
            value = struct.unpack_from('!d', msg, offset)[0]
            offset += struct.calcsize('!d')
            self.assertEqual(value, data)
        msg_index += 1

        # Simulate Session Shutdown
        self.delegate.session_did_shutdown()
        msg = self.mock_socket.sendall.call_args_list[msg_index][P_ARGS][0]
        self.assertTrue(is_reset(msg))
        msg_index += 1
        msg = self.mock_socket.sendall.call_args_list[msg_index][P_ARGS][0]
        self.assertEqual(struct.unpack('!q', msg)[0], houdini.commands.DISCONNECT)


def is_reset(msg):
    raw_msg = struct.unpack_from('!8B', msg)
    if not raw_msg[0] == 170:
        return False

    for index in range(0, 8, 2):
        if not (raw_msg[index], raw_msg[index+1],) == (170, 0):
            return False
    return True


def check_channel_name(msg, offset, expected_name, expected_chunks):
    chunks = struct.unpack_from('!q', msg, offset)[0]
    offset += struct.calcsize('!q')
    assert 1 == expected_chunks

    string = struct.unpack_from('!8s', msg, offset)[0].strip(' \t\r\n\0')
    offset += struct.calcsize('!8s')
    assert str(string) == str(expected_name), "'{0}' != '{1}'".format(string, expected_name)

    return offset

