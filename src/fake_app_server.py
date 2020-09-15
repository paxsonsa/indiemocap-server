from Queue import Queue
import time
from math import sin, cos

class HoudiniPipeInServer:

    COMMAND = {
        'value': 1,
        'upload': 2,
        'names': 3,
        'disconnect': 4,
        'refresh': 5,
        'script': 6
    }

    def __init__(self, queue):
        self.queue = queue

    def serve(self, port):
        while True:


def main():

    while True:
        sendNames(client, ['tx', 'ty'])
        t = 0
        while running:
            sendValue(client, [sin(t), cos(t)])
            t += 0.03
            time.sleep(0.03)

if __name__ == "__main__":
    main()
