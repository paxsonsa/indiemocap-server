# Copyright (c) 2020 Andrew Paxson. All rights reserved.
# This file is subject to the terms and conditions defined in
# file 'LICENSE.md', which is part of this source code package
""" server.py
Main Server Runtime for IndieMocap

Author: Andrew Paxson
"""
import netifaces
import socket
import threading
from zeroconf import ServiceInfo, Zeroconf

import indiemocap as imc
import indiemocap.session_delegates.echo as echo_delegate
import indiemocap.log
import indiemocap.message_types


class MocapServer(imc.connection_delegates.ConnectionDelegate):

    def __init__(self, session_controller):
        self.session_controller = session_controller
        self.configure_transport()
        self.configure_server()

    def configure_transport(self):
        self.transport = imc.transport.ProtocolTransport()
        self.transport.register_handlers(imc.default_handlers)

    def configure_server(self):
        sock = make_udp_socket()
        host, port = sock.getsockname()
        hostname = socket.gethostname()

        desc = {}

        self._service_info = ServiceInfo("_indieengine._udp.local.",
                        "{}._indieengine._udp.local.".format(hostname),
                        address=get_socket_addr(),
                        port=port,
                        properties=desc
        )
        self._zeroconf = Zeroconf()

        print("Service available on port {0}".format(port))
        print("Registration of a service, press Ctrl-C to exit...")
        self._zeroconf.register_service(self._service_info)

        # Assign Connection
        self.connection = imc.connection.UDPConnection(sock, self.transport, self)

    def start_threaded_connection(self):
        close_event = threading.Event()
        t = threading.Thread(name='server',
                             target=self.connection.connection_thread_worker,
                             args=(self.connection, close_event))
        t.start()
        return close_event

    def shutdown(self):
        self.connection.close()
        self._zeroconf.unregister_service(self._service_info)
        self._zeroconf.close()

    def did_recieve_message(self, message):
        response = None
        if message.mtype == indiemocap.message_types.SessionInit:
            response = self.session_controller.initialize_session(
                message.serialize()
            )
        elif message.mtype == indiemocap.message_types.SessionHeartbeat:
            response = self.session_controller.make_heartbeat()

        elif message.mtype == indiemocap.message_types.MotionData:
            pass
            # response = self.session_controller.process_motion_data(message)
        else:
            print(message)
        return response


def make_udp_socket():
    """Returns a new udp socket bound to 0.0.0.0 and with kernel choosen port."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', 8877,))
    sock.setblocking(False)
    return sock


def get_socket_addr():
    """Returns network IP for this host from the network interfaces

    127.0.0.1 is excluded.

    Returns:
        socket bytes
    """
    valid_addrs = [netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr']
                   for i in netifaces.interfaces()
                   if netifaces.AF_INET in netifaces.ifaddresses(i)]

    for addr in valid_addrs:
        if not addr.startswith('127.0'):
            return socket.inet_aton(addr)


def run_dev_server():
    indiemocap.log.get_logger()
    session = imc.session.Session()
    delegate = echo_delegate.EchoSessionDelegate()
    session_controller = imc.session_controller.SessionController(
        session,
        delegate
    )
    start_server_with(session_controller)


def start_server_with(session_controller):
    logger = indiemocap.log.get_logger()
    server = MocapServer(session_controller)
    try:
        logger.info("Launching Server...")
        close_event = server.start_threaded_connection()
        while True:
            pass

    except KeyboardInterrupt:
        pass

    finally:
        logger.info("Closing...")
        close_event.set()
        server.shutdown()




if __name__ == "__main__":
    run_dev_server()
