import cv2
from threading import Thread
from robotControl import motorControl
import re
from time import sleep
import pyzbar.pyzbar as pyzbar
import numpy as np

debug_bbox = True
qrSizeThreshold = 200

class qrDetector(object):
    def __init__(self, fr):
        self.started = False
        self.fr = fr
        self.frame = self.fr.read()
        self.result = ''
        self.motor = motorControl()
        self.lastCurID = -1
        self.lastNextID = 0
        self.motor.start()
        self.detector = cv2.QRCodeDetector()
        self.thread = Thread(target=self.detect, args=())
        self.thread.daemon = True

    def start(self):
        self.started = True
        self.thread.start()

    def detect(self):
        sleep(3)
        while self.started:
            self.motor.move('F')
            self.frame = self.fr.read()
            data = ''
            distX = 0
            decodedObjects = pyzbar.decode(self.frame)
            for obj in decodedObjects:
                print("type: ", obj.type)
                print("data: ", obj.data)   
                if obj.type == 'QRCODE':
                    data = str(obj.data, 'utf-8')
                    points = obj.polygon
                    distX = np.max(points, axis=0)[0] - np.min(points, axis=0)[0]
                    print(distX)
                    # Draw the convext hull
                    if debug_bbox == True:
                         # Number of points in the convex hull
                        n = len(points)
                        for j in range(0, n):
                            cv2.line(self.frame, points[j], points[(
                                j+1) % n], (255, 0, 0), 3)
                        
            if distX > 0:
                print("qr size: ", distX)
                if re.match(r"\[[0-9]+,[LRBS],[0-9]+\]", data):
                    if distX < qrSizeThreshold:
                        self.motor.move('F')
                    else:
                        self.motor.stop()
                        self.motor.move('S')

                        data = data.strip("[]")
                        data = data.split(',')
                        curID = int(data[0])

                        if self.lastCurID != curID:
                            if curID == self.lastNextID:
                                if data[1] == 'S':
                                    self.stop()
                                else:
                                    self.lastCurID = curID
                                    self.lastNextID = int(data[2])
                                    self.motor.move(data[1])
            # while self.motor.isTurning():
            #     sleep(0.001)
            sleep(0.03)

    def read(self):
        return self.frame
        

    def stop(self):
        self.started = False
        self.motor.stop()
        self.motor.motorDeinit()


                
            


            
                    


