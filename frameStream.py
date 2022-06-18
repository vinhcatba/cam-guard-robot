from threading import Thread, Lock
import socket
import pickle
import struct
import time

from frameGet import FrameGet


# todo: frameStream should be a thread too


class FrameStream(object):
    def __init__(self, cap, host='localhost', port=8089):
        #self.cap = FrameGet().start()
        self.started = False
        self.cap = cap
        self.host = host
        self.port = port
        self.clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clientsocket.connect((self.host, self.port))
        self.payload_size = struct.calcsize("=L") ### CHANGED
        print("payload size ", self.payload_size)

    
    def start(self):
        
        if self.started:
            print("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.sendstream, args=())
        self.thread.start()
        return self

    def sendstream(self):

        
        while self.started:
            #ret,frame=cap.read()
            frame = self.cap.read()
            # Serialize frame
            data = pickle.dumps(frame)

            # Send message length first
            message_size = struct.pack("=L", len(data)) ### CHANGED
            # print("msg size ", message_size)
            # Then data
            self.clientsocket.sendall(message_size + data)
            
            time.sleep(0.03)
        # msg_size = struct.pack("L", "-9999")
        # self.clientsocket.sendall(msg_size)
        
    
    def stop(self):
        self.started = False
        self.thread.join()
        self.clientsocket.close()

