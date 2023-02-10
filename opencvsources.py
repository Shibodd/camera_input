import cv2
import numpy as np
import time
class OpenCVError(Exception):
    '''An error caused by OpenCV'''
    pass

class OpenCVCameraFrameSource:
    def __init__(self, captureIndex, captureApi, width, height, fps):
        self.captureIndex = captureIndex
        self.captureApi = captureApi
        self.width = width
        self.height = height
        self.fps = fps
        self.__last_frame = None
        self.__last_frame_ns = 0

    def __enter__(self):
        self.cap = cv2.VideoCapture(self.captureIndex, self.captureApi)
        if not self.cap.isOpened():
            raise OpenCVError("Error while opening the capture.")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)

        print("Camera running!") 
        return self

    def __exit__(self, *args):
        self.cap.release()
        self.cap = None
        print("Camera stopped!")

    def __next__(self):
        t = time.time_ns()
        if t - self.__last_frame_ns > 1_000_000_000 / self.fps:
            ok = self.cap.grab()
            if not ok:
                raise OpenCVError("Failed to grab a frame from the capture.")

            ns = time.time_ns()

            ok, frame = self.cap.retrieve()
            if not ok:
                raise OpenCVError("Failed to retrieve the frame from the capture.")

            self.__last_frame = frame
            self.__last_frame_ns = ns

        return (self.__last_frame_ns, self.__last_frame)

    def __iter__(self):
        return self

class BasicPointSource:
    def __init__(self, frameSource):
        self.frameSource = frameSource
        self.green_min_range = np.array([0,0,145])
        self.green_max_range = np.array([255,115,255])
        self.red_min_range = np.array([0,145,160])
        self.red_max_range = np.array([255,255,255])

        self.__last_red = None
        self.__last_green = None
        self.__last_ns = None
        self.__last_frame = None

    def __next__(self):
        (ns, frame) = next(self.frameSource)

        if ns == self.__last_ns:
            return (self.__last_frame, self.__last_red, self.__last_green)
        else:
            self.__last_ns = ns
            self.__last_frame = frame

        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        
        def process(min_range, max_range):
            im = cv2.inRange(lab, min_range,max_range)
            pts = cv2.findNonZero(im)
            if pts is not None:
                return np.mean(pts, axis=(0, 1))
            else:
                return None

        self.__last_red = process(self.red_min_range, self.red_max_range)
        self.__last_green = process(self.green_min_range, self.green_max_range)
        return (
            frame,
            self.__last_red,
            self.__last_green
        )

    def __iter__(self):
        return self