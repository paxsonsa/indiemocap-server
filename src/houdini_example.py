#! /usr/bin/env python
import sys
import struct
import socket
import time
from threading import Thread
from math import sin, cos
from array import array
from random import random

ESC = chr(170) #0xAA
NUL = chr(0)

COMMAND = {
    'value': 1,
    'upload': 2,
    'names': 3,
    'disconnect': 4,
    'refresh': 5,
    'script': 6
}

threads = []
running = True

def send(c, binary):
    for b in binary:
        if b == ESC:
            c.send(b)
        c.send(b)

def sendValue(c, data):
    sendReset(c)
    send(c, struct.pack('!qq', COMMAND['value'], len(data)))
    for d in data:
        send(c, struct.pack('!d', d))

def sendUpload(c, length, rate, start, channels, data):
    sendReset(c)
    send(c, struct.pack('!qqddq',
                        COMMAND['upload'],
                        length,
                        rate,
                        start,
                        channels))
    for d in data:
        send(c, struct.pack('!d', d))

def sendNames(c, names):
    sendReset(c)
    send(c, struct.pack('!qq', COMMAND['names'], len(names)))
    for name in names:
        (name, chunks) = padString(name)
        send(c, struct.pack('!q', chunks))
        send(c, name)

def disconnect(c, channels, data):
    sendReset(c)
    send(c, struct.pack('!q', COMMAND['disconnect']))

def sendRefresh(c, delay):
    sendReset(c)
    send(c, struct.pack('!qq', COMMAND['refresh'], delay))

def sendScript(c, script):
    sendReset(c)
    (script, chunks) = padString(script)
    send(c, struct.pack('!qq', COMMAND['script'], chunks))
    send(c, script)

def sendReset(c):
    c.send(struct.pack('8s', (ESC + NUL) * 4))

def padString(s):
    chars = len(s)
    chunks = chars / 8
    padding = chars % 8

    if padding:
        chunks += 1
        s += NUL * (8 - padding)
    return (s, chunks)

def connection(client, worker):
    while running:
        try:
            worker(client)
        except socket.error:
            client.close()
            return

    client.shutdown(socket.SHUT_RDWR)
    time.sleep(0.15)
    client.close()

def example(client):
    sendNames(client, ['tx', 'ty'])
    t = 0
    while running:
        sendValue(client, [sin(t), cos(t)])
        t += 0.03
        time.sleep(0.03)

class HoudiniConnection(Thread):
    def __init__(self, port, worker):
        Thread.__init__(self)
        self.socket = socket.socket()
        self.port = port
        self.worker = worker

    def run(self):
        global running
        s = self.socket
        host = 'localhost'
        port = self.port

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print('Starting server %s:%d' % (host, port))
        try:
            s.bind((host, port))
            s.listen(1)
        except socket.error as e:
            print('Unable to bind socket:', e)
            s.close()
            return

        while running:
            try:
                client, addr = s.accept()
            except socket.error:
                break
            print('Connected', addr)
            t = Thread(target=connection, args=[client, self.worker])
            t.start()
            threads.append(t)

        running = False
        for t in threads:
            t.join()
        s.close()

    def close(self):

        self.socket.close()

if __name__ == '__main__':
    pipe = HoudiniConnection(5000, example)
    pipe.start()
    raw_input('Wait 5 sec, Ctrl-c.\n')
    pipe.close()
