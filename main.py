
from pickletools import int4
from frameGet import FrameGet
from frameStream import FrameStream
import time
import cv2

cap = FrameGet().start()
frameStreamObj = FrameStream().start( cap, host='10.2.204.121')
detector = cv2.QRCodeDetector()

while True:
    time.sleep(0.03)
    frame = cap.read()
    #frame = cv2.resize(frame,(frame.shape[1], frame.shape[0]), 0.5, 0.5, interpolation = cv2.INTER_AREA )
    #detect and decode

    data, bbox, _ = detector.detectAndDecode(frame)
    if data:
        print(data)
    # check if there is a QRCode in the image
    if bbox is not None:
        # display the image with bboxesN
        
        for i in range(len(bbox)):

            arr = bbox[i].astype(int)
            max_x = max(arr, key = lambda x: x[0])
            min_x = min(arr, key = lambda x: x[0])
            max_y = max(arr, key = lambda x: x[1])
            min_y = min(arr, key = lambda x: x[1])
            pt1 = (max_x[0], max_y[1])
            pt2 = (min_x[0], min_y[1])

            cv2.rectangle(frame, pt1, pt2, (0,255,0), 2)
        if data:
            print(data)
            cv2.putText(frame, data, tuple(arr[0]-20), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(255,0,200), thickness=1)

    # display the result
    cv2.imshow("qr detect", frame)
    
    if cv2.waitKey(1) == ord("q"):
        break
    
cap.stop()
frameStreamObj.stop()
cv2.destroyAllWindows()

