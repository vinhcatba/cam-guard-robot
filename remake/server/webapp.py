import socket
from flask import Flask, render_template, Response
from receiver import frameReceiv
from detect import Detector
import cv2

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
fr = frameReceiv(s, addr='', port=8080)
fr.start()
detector = Detector(fr)
detector.start()

app = Flask(__name__)


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')


def gen_frame():
    """Video streaming generator function."""
    while True:
        frame = detector.read()
        # frame = cap.read()
        convert = cv2.imencode('.jpg', frame)[1].tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + convert + b'\r\n')  # concate frame one by one and show result


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':

    app.run(host='0.0.0.0', threaded=True)
