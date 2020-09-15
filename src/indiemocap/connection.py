# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" connection.py
A module defining the UDP Connections

Author: Andrew Paxson
"""
import errno
import socket


class UDPConnection:

    max_size = 4 * 1024  # Buffer size passed to recv()

    class Metadata:
        def __init__(self):
            self._metadata = {}

        def update_metadata(self, **key_values):
            for key, value in key_values.items():
                self._metadata[key] = value

        def get(self, key):
            return self._metadata.get(key)

    @staticmethod
    def connection_thread_worker(connection, event):
        connection.start(event)

    def __init__(self, sock, transport, connection_delegate):
        self.sock = sock
        self.transport = transport
        self.transport.connection = self
        self.metadata = self.Metadata()
        self.delegate = connection_delegate
        self.metadata.update_metadata(socket=sock)

    def start(self, close_event):
        print("starting server")
        while not close_event.is_set():
            try:
                data, host_port = self.sock.recvfrom(self.max_size)
            except socket.error as error:
                if error.errno != errno.EAGAIN:
                    raise error
            else:
                self.metadata.update_metadata(host_port=host_port)
                message, error_msg = self.transport.handled_recieved(data, self.metadata)

                # Message failed to be decoded, send error from transport layer.
                if error_msg:
                    self.send_message(error_msg)
                    continue

                # Pass message to delegate to be processed and send the response.
                if self.delegate and message:
                    response = self.delegate.did_recieve_message(message)
                    if response:
                        self.send_message(response)

    def close(self):
        self.sock.close()

    def send_message(self, message):
        encoded_message = self.transport.handle_send(message, self.metadata)
        self.sock.sendto(encoded_message, self.metadata.get("host_port"))
