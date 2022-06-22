from __future__ import division
from ast import arg
import cv2
from threading import Thread
import numpy as np
import socket
import struct
import math



class frameRead(object):
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)
        if self.cap.isOpened() is False:
            print("cannot open capture, exiting")
            exit(0)
        # reading a single frame from vcap stream for initializing
        self.grabbed, self.frame = self.cap.read()
        if self.grabbed is False:
            print('[Exiting] No more frames to read')
            exit(0)
        self.started = False
        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
    
    def start(self):
        self.started = True
        self.thread.start()

    def update(self):
        while self.started:
            self.grabbed, self.frame = self.cap.read()
            if self.grabbed is False:
                print('[Exiting] No more frames to read')
                self.started = False
                break
        self.cap.release()

    def read(self):
        return self.frame

    def stop(self):
        self.started = False

class FrameSegment(object):
    """ 
    Object to break down image frame segment
    if the size of image exceed maximum datagram size 
    """
    MAX_DGRAM = 2**16
    MAX_IMAGE_DGRAM = MAX_DGRAM - 64 # extract 64 bytes in case UDP frame overflown
    def __init__(self, fr, sock, port, addr="127.0.0.1", quality=50):
        self.s = sock
        self.port = port
        self.addr = addr
        self.fr = fr
        self.quality = [
            int(cv2.IMWRITE_JPEG_QUALITY), quality
        ]
        self.started = False

        self.thread = Thread(target=self.frameStream, args=())
        self.thread.daemon = True

    def start(self):
        self.started = True
        self.thread.start()
        
    def udp_frame(self, img):
        """ 
        Compress image and Break down
        into data segments 
        """
        compress_img = cv2.imencode('.jpg', img, self.quality)[1]
        dat = compress_img.tobytes()
        size = len(dat)
        count = math.ceil(size/(self.MAX_IMAGE_DGRAM))
        array_pos_start = 0
        while count:
            array_pos_end = min(size, array_pos_start + self.MAX_IMAGE_DGRAM)
            self.s.sendto(struct.pack("=B", count) +
                dat[array_pos_start:array_pos_end], 
                (self.addr, self.port)
                )
            array_pos_start = array_pos_end
            count -= 1

    def frameStream(self):
        while self.started:
            self.frame = self.fr.read()
            self.udp_frame(self.frame)
        self.s.close()

    def stop(self):
        self.started = False

