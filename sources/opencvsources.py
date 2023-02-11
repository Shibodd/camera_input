import cv2
import time

class OpenCVError(Exception):
    '''An error caused by OpenCV'''
    pass

class OpenCVCameraFrameSource:
    def __init__(self, captureIndex, captureApi, width, height, fps):
        self.__captureIndex = captureIndex
        self.__captureApi = captureApi
        self.__width = width
        self.__height = height
        self.__fps = fps
        
        self.__last_frame = None
        self.__last_frame_ns = 0

    def __enter__(self):
        self.cap = cv2.VideoCapture(self.__captureIndex, self.__captureApi)
        if not self.cap.isOpened():
            raise OpenCVError("Error while opening the capture.")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.__width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.__height)
        self.cap.set(cv2.CAP_PROP_FPS, self.__fps)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        print("Camera running!") 
        return self

    def __exit__(self):
        self.cap.release()
        self.cap = None
        print("Camera stopped!")

    def tick(self):
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

    def __next__(self):
        return (self.__last_frame_ns, self.__last_frame)

    def __iter__(self):
        return self