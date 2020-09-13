# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" houdini_session_delegate.py
A Session Controller Delegate Specialized for Houdini.

Author: Andrew Paxson
"""
import socket

import indiemocap.session

class HoudiniSessionControllerDelegate:

    def __init__(self, pipe_port=5555):
        self.socket = socket.socket()
        self.pipe_port = pipe_port

    def sessionDidInitialize(self, client_info):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.socket.bind(('localhost', self.pipe_port))
            self.socket.listen(1)
        except socket.error as e:
            print('Unable to bind socket:', e)
            self.socket.close()
            # TODO Send Error to Controller
            return
        self.socket.accept()

    def modeDidChange(self, mode):
        if mode == indiemocap.session.modes.Stop:
            pass
        elif mode == indiemocap.session.modes.Live:
            pass
        elif mode == indiemocap.session.modes.Record:
            pass
        else:
            # TODO send error
            pass

    def didRecieveMotionData(self, motion_data):
        print(motion_data)


    def sessionDidShutdown(self):
        self.socket.close()
        return
