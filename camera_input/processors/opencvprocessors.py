import cv2
import numpy as np
import time

from camera_input.processors.processors import Processor, cached_processor

@cached_processor
class ColorConverterProcessor(Processor):
    """ A frame source which applies the colorspace conversion."""

    def __init__(self, frameSource, colorConversion):
        super().__init__(frameSource)
        self.colorConversion = colorConversion
    
    def process(self, _, frame):
        result = frame[0]
        return (time.monotonic_ns(), cv2.cvtColor(result, self.colorConversion))

@cached_processor
class BlurProcessor(Processor):
    """ A frame source which blurs the input frame."""

    def __init__(self, frameSource, radii, sigma):
        super().__init__(frameSource)
        self.radii = radii
        self.sigma = sigma
        
    def process(self, _, results):
        frame = results[0]
        return (time.monotonic_ns(), cv2.GaussianBlur(frame, (self.radii, self.radii), self.sigma))

@cached_processor
class SimpleColorRangePointProcessor(Processor):
    """ A point source which averages the coordinates of the points which have (opencv)  colors in the range(s) passed as parameter.
        If multiple ranges are passed, the results of each individual inRange will be OR'd."""

    def __init__(self, frameSource, ranges):
        """ Ranges: a list of color ranges in the form [(min, max), (min, max), ...]. """
        super().__init__(frameSource)
        self.ranges = ranges

    def process(self, _, results):
        frame = results[0]
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
            res = np.mean(pts, axis=(0, 1))
        else:
            res = None

        return (time.monotonic_ns(), res)