
from __future__ import division
import cv2
import numpy as np
import socket
import struct
from threading import Thread

MAX_DGRAM = 2**16

class frameReceiv(object):
    def __init__(self, socket, addr='localhost', port=8080):
        self.addr = addr
        self.port = port
        self.s = socket
        self.s.bind((self.addr, self.port))
        self.data = b''
        self.frameBytes = b''
        self.dump_buffer()
        self.frame = self.get_first_frame()
        self.started = False
        self.thread = Thread(target=self.receive, args=())
        self.thread.daemon = True

    def get_first_frame(self):
        received = False
        seg, addr = self.s.recvfrom(MAX_DGRAM)
        data = b''
        while received is not True:
            if struct.unpack("=B", seg[0:1])[0] > 1:
                data += seg[1:]
            else:
                data += seg[1:]
                frame = cv2.imdecode(
                    np.frombuffer(data, dtype=np.uint8), 1)
                received = True
                break
        return frame

    def start(self):
        self.started = True
        self.thread.start()

    def dump_buffer(self):
        """ Emptying buffer frame """
        while True:
            seg, addr = self.s.recvfrom(MAX_DGRAM)
            print(seg[0])
            if struct.unpack("B", seg[0:1])[0] == 1:
                print("finish emptying buffer")
                break

    def receive(self):
        """ Getting image udp frame &
        concate before decode and output image """

        while self.started:
            seg, addr = self.s.recvfrom(MAX_DGRAM)
            
            if struct.unpack("=B", seg[0:1])[0] > 1:
                self.data += seg[1:]
            else:
                self.data += seg[1:]
                self.frameBytes = self.data
                self.frame = cv2.imdecode(np.frombuffer(self.data, dtype=np.uint8), 1)
                self.data = b''

        self.s.close()

    def read(self):
        return self.frame

    def readAsBytes(self):
        return self.frameBytes

    def stop(self):
        self.started = False
