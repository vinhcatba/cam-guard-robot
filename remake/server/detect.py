import cv2
import os

from pycoral.adapters.common import input_size
from pycoral.adapters.detect import get_objects
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.utils.edgetpu import run_inference


from server import SocketRecv
from threading import Thread, Lock

import time


class Detector(object):
    def __init__(self, fr, default_model_dir='../temp/all_models', 
            default_model = 'mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite', 
            default_labels = 'coco_labels.txt',
            threshold = 0.1,
            top_k = 5):
        self.default_model_dir = default_model_dir
        self.default_model = default_model
        self.default_labels = default_labels

        self.fr = fr
        
        self.started = False
        self.read_lock = Lock()
        self.frame = self.fr.read()

        print('Loading {} with {} labels.'.format(self.default_model,
                                                  self.default_labels))
        self.interpreter = make_interpreter(os.path.join(self.default_model_dir,
                                                         self.default_model))
        self.interpreter.allocate_tensors()
        self.labels = read_label_file(os.path.join(self.default_model_dir,
                                                   self.default_labels))
        self.inference_size = input_size(self.interpreter)
        self.threshold = threshold
        self.top_k = top_k
        self.thread = Thread(target=self.detect, args=())
        self.thread.daemon = True

    def start(self):
        if self.started:
            print("already started")
            return None
        self.started = True
        self.thread.start()

    def detect(self):
        while self.started:
            self.frame = self.fr.read()

            cv2_im_rgb = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
            cv2_im_rgb = cv2.resize(cv2_im_rgb, self.inference_size)
            run_inference(self.interpreter, cv2_im_rgb.tobytes())
            objs = get_objects(self.interpreter, self.threshold)[:self.top_k]
            self.read_lock.acquire()
            self.frame = self.append_objs_to_img(
                self.frame, self.inference_size, objs, self.labels)
            self.read_lock.release()
            time.sleep(0.03)

    def append_objs_to_img(self, cv2_im, inference_size, objs, labels):
        height, width, channels = cv2_im.shape
        scale_x, scale_y = width / \
            inference_size[0], height / inference_size[1]
        for obj in objs:
            bbox = obj.bbox.scale(scale_x, scale_y)
            x0, y0 = int(bbox.xmin), int(bbox.ymin)
            x1, y1 = int(bbox.xmax), int(bbox.ymax)

            percent = int(100 * obj.score)
            label = '{}% {}'.format(percent, labels.get(obj.id, obj.id))

            cv2_im = cv2.rectangle(cv2_im, (x0, y0), (x1, y1), (0, 255, 0), 2)
            cv2_im = cv2.putText(cv2_im, label, (x0, y0+30),
                                 cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)
        return cv2_im

    def read(self):
        return self.frame

    def stop(self):
        self.started = False
        self.thread.join()
