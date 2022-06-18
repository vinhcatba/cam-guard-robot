from flask import Flask, render_template, Response
from server import SocketRecv
from detect import Detector
import cv2
app = Flask(__name__)

cap = Detector().start()
# cap = SocketRecv().start()

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen_frame():
    """Video streaming generator function."""
    while cap:
        frame = cap.getOutputFrame()
        # frame = cap.read()
        convert = cv2.imencode('.jpg', frame)[1].tobytes()
        convert = cap.getOutputFrame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n') # concate frame one by one and show result


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)