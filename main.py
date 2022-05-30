
from frameGet import FrameGet
from frameStream import FrameStream

import cv2

cap = FrameGet().start()
frameStreamObj = FrameStream().start( cap, host='10.2.204.120')

while True:
    frame = cap.read()
    cv2.imshow('frame source', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
cap.stop()
frameStreamObj.stop()
cv2.destroyAllWindows()

