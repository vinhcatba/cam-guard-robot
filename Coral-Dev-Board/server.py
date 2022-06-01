import pickle
import socket
import struct
from threading import Thread, Lock
import numpy as np

import cv2
import time


HOST = ''
PORT = 8089

class SocketRecv(object):
    def __init__(self):
        self.started = False
        self.frame = b''
        self.read_lock = Lock()

    def start(self):
        if self.started:
            print("already started")
            return None
        self.started = True
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Socket created')

        self.s.bind((HOST, PORT))
        print('Socket bind complete')
        self.s.listen(10)
        print('Socket now listening')

        self.conn, self.addr = self.s.accept()
        self.data = b'' ### CHANGED
        self.payload_size = struct.calcsize("L") ### CHANGED
        self.thread = Thread(target=self.sockrecv, args=())
        self.thread.start()
        return self

    def sockrecv(self):
        while self.started:
            # Retrieve message size
            while len(self.data) < self.payload_size:
                self.data += self.conn.recv(4096)

            self.packed_msg_size = self.data[:self.payload_size]
            self.data = self.data[self.payload_size:]
            self.msg_size = struct.unpack("L", self.packed_msg_size)[0] ### CHANGED
            
            # Retrieve all data based on message size
            while len(self.data) < self.msg_size:
                self.data += self.conn.recv(4096)

            self.frame_data = self.data[:self.msg_size]
            self.data = self.data[self.msg_size:]
            if not self.data:
                print("socket closed by client")
                break
                
            # Extract frame
            self.read_lock.acquire()
            self.frame = pickle.loads(self.frame_data)
            self.read_lock.release()
            time.sleep(0.03)
    
    def read(self):
        self.read_lock.acquire()
        frameCopied = self.frame.copy()
        self.read_lock.release()
        return frameCopied

    def stop(self):
        self.stared = False
        self.thread.join()
        self.conn.close()
