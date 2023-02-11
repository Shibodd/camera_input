import cv2
import numpy as np
import math

class Protractor:
    def __init__(self, west_source, east_source):
        self.west_source = west_source
        self.east_source = east_source
        self.mat = np.zeros([512, 512, 3], dtype=np.uint8)

    def __enter__(self):
        cv2.imshow(str(id(self)), self.mat)
        cv2.setWindowTitle(str(id(self)), "Protractor")
        return self
    def __exit__(self, *args):
        cv2.destroyWindow(str(id(self)))

    def tick(self):
        _, w = next(self.west_source)
        _, e = next(self.east_source)

        if w is None or e is None:
            return

        delta = e - w
        theta = math.atan2(delta[1], delta[0])

        a = np.array([math.cos(theta), math.sin(theta)]) * 256
        b = -a

        center = np.array(self.mat.shape[0:2]) / 2
        a = a + center
        b = b + center

        self.mat = cv2.rectangle(self.mat, (0, 0), self.mat.shape[0:2], (0, 0, 0), -1)
        cv2.line(self.mat, a.astype(np.uint16), b.astype(np.uint16), (255, 0, 0), 3)
        cv2.imshow(str(id(self)), self.mat)