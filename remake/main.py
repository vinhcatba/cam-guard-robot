
import socket
import cv2
from camReadAndStream import frameRead, FrameSegment
from robotControl import motorControl
from qrDetectAndMove import qrDetector
from time import sleep

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 8080
    fr = frameRead()
    fr.start()
    fs = FrameSegment(fr, s, port, addr='192.168.1.23')
    fs.start()
    qrdet = qrDetector(fr)
    qrdet.start()
    # motor = motorControl()
    # motor.start()
    sleep(4)
    while True:

        frame = qrdet.read()
        cv2.imshow("frame", frame)
        if cv2.waitKey(33) == ord('q'):
            break
    fr.stop()
    qrdet.stop()
    cv2.destroyAllWindows

if __name__ == "__main__":
    main()