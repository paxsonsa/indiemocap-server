# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" session.py
Module containing session data

Author: Andrew Paxson
"""


class Session:

    class modes:
        """ Modes in which the session can be in

        Attributes:
            Stop: No motion data being sent or recording is being performed.
            Live: Motion data is being sent but nothing is recording.
            Record: Motion data is being sent and recording.
        """
        Stopped = 0
        Live = 1
        Record = 2

    def __init__(self):
        self.reset()

    def reset(self):
        self.client_info = None
        self.mode = self.modes.Stopped
        self.samples = 60
        self.current_take = 0
        self.takes = 1
        self.supports_video = False
