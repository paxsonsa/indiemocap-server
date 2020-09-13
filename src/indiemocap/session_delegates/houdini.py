# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" houdini.py
A Session Controller Delegate Specialized for Houdini.
Author: Andrew Paxson
"""
import socket
import struct

import indiemocap.session

class HoudiniSessionControllerDelegate:

    def __init__(self, pipe_port=5555):
        self.socket = socket.socket()
        self.pipe_port = pipe_port

    def session_did_initialize(self, client_info):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.socket.connect(('127.0.0.1', self.pipe_port))
        except socket.error as e:
            print('Unable to bind socket:', e)
            self.socket.close()
            # TODO Send Error to Controller
            return

        # When the connection is made, setup the channel names
        send_channel_names(
            self.socket,
            [
                "yaw",
                "pitch",
                "roll",
                "accX",
                "accY",
                "accZ",
            ]
        )

    def mode_did_change(self, mode):
        if mode == indiemocap.session.modes.Stop:
            pass
        elif mode == indiemocap.session.modes.Live:
            pass
        elif mode == indiemocap.session.modes.Record:
            pass
        else:
            # TODO send error
            pass

    def did_recieve_motion_data(self, motion_data):
        send_value(
            self.socket,
            [motion_data.yaw, motion_data.pitch, motion_data.roll,
             motion_data.accX, motion_data.accY, motion_data.accZ]
        )



    def session_did_shutdown(self):
        send_disconnect(self.socket)
        self.socket.close()
        return

ESC = chr(170)
NULL = chr(0)

class commands:
    VALUE = 1
    UPLOAD = 2
    NAMES = 3
    DISCONNECT = 4
    REFRESH = 5
    SCRIPT = 6


def send_disconnect(conn):
    send_reset(conn)
    conn.sendall(struct.pack('!q', commands.DISCONNECT));

def send_reset(conn):
    conn.sendall(struct.pack('!8c', ESC, NULL, ESC, NULL, ESC, NULL, ESC, NULL))

def send_value(conn, values):
    send_reset(conn)
    msg = struct.pack('!qq', commands.VALUE, len(values))
    msg += struct.pack('!' + 'd' * len(values), *values)
    conn.sendall(msg)

def send_channel_names(conn, names):
    send_reset(conn)
    msg = b''
    msg += struct.pack('!qq', commands.NAMES, len(names))

    for name in names:
        name, chunks = pad_string(name)
        msg += struct.pack('!q', chunks)
        msg += name
    conn.sendall(msg)


def pad_string(s):
    chars = len(s)
    chunks = chars / 8
    padding = chars % 8

    if padding:
        chunks += 1
        s += NULL * (8 - padding)
    return s, chunks
