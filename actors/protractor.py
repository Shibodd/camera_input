import cv2
import numpy as np
import math

class Protractor:
    TEXT_FONT = cv2.FONT_HERSHEY_PLAIN
    TEXT_SIZE = 1
    TEXT_THICKNESS = 1
    TEXT_COLOR = (255, 255, 255)
    TEXT_MARGIN = 10

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

    def act(self):
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

        theta_deg = math.degrees(theta)
        text = f"{theta_deg:.0f} deg"
        size = cv2.getTextSize(text, self.TEXT_FONT, self.TEXT_SIZE, self.TEXT_THICKNESS)
        cv2.putText(self.mat, text, (self.TEXT_MARGIN, size[1] + self.TEXT_MARGIN), self.TEXT_FONT, self.TEXT_SIZE, self.TEXT_COLOR, self.TEXT_THICKNESS)

        cv2.imshow(str(id(self)), self.mat)