import cv2
import numpy as np

from processors.processors import CachedProcessor

class ColorConverterProcessor(CachedProcessor):
    def __init__(self, frameSource, colorConversion):
        super().__init__(frameSource)
        self.colorConversion = colorConversion
    
    def process(self, result):
        return cv2.cvtColor(result, self.colorConversion)


class BlurProcessor(CachedProcessor):
    def __init__(self, frameSource, radii):
        super().__init__(frameSource)
        self.radii = radii
    def process(self, frame):
        return cv2.blur(frame, (self.radii, self.radii))
class SimpleColorRangePointProcessor(CachedProcessor):
    """ A point source which averages the coordinates of the points which have (opencv)  colors in the range(s) passed as parameter.
        If multiple ranges are passed, the results of each individual inRange will be OR'd."""

    def __init__(self, frameSource, ranges):
        """ Ranges: a list of color ranges in the form [(min, max), (min, max), ...]. """
        super().__init__(frameSource)
        self.ranges = ranges

    def process(self, frame):
        if len(self.ranges) <= 1: # fast path
            min_range, max_range = self.ranges[0]
            im = cv2.inRange(frame, min_range,max_range)
        else:
            im = cv2.inRange(frame, *self.ranges[0])
            for i in range(1, len(self.ranges)):
                min_range, max_range = self.ranges[i]
                im = cv2.bitwise_or(im, cv2.inRange(frame, min_range, max_range))

        pts = cv2.findNonZero(im)
        if pts is not None:
            return np.mean(pts, axis=(0, 1))
        else:
            return None