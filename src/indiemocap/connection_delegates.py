# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" connection_delegates.py
ConnectionDelegate

Author: Andrew Paxson
"""
from indiemocap import message_types
from indiemocap.handshakes import HandshakeMessage

class ConnectionDelegate:

    def did_recieve_message(self, message):
        raise NotImplementedError



class EchoConnectionDelegate(object):

    def did_recieve_message(self, message):
        print("Recieved:", message)

    def did_send_message(self, message):
        print("Sent:", message)

