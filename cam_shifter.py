import cv2
import numpy as np
import functools

class OpenCVError(Exception):
    '''An error caused by OpenCV'''
    pass



def openCvCaptureProperty(attributeName, cvPropertyId, defaultValue):
    def decorator(Class):
        privateName = "__" + attributeName

        def getter(self):
            return getattr(self, privateName)

        def setter(self, value): 
            setattr(self, privateName, value)

        setattr(Class, attributeName, property(getter, setter))
        return Class


class BasicOpenCVPointReader:
    def __init__(self):
        pass

    def __enter__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise OpenCVError("Errore durante l'apertura dell'obbiettivo")

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 352)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)
        self.cap.set(cv2.CAP_PROP_FPS, 60)

        
        print("Camera running!") 
        return self

        #self.cap.set(0, 0)

    def __exit__(self, *args):
        self.cap.release()
        self.cap = None
        print("Camera stopped!")

    def __next__(self):
        _, frame = self.cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        red_mask1 = cv2.inRange(hsv, np.array([0,50,240]), np.array([20,255,255]))
        red_mask2 = cv2.inRange(hsv, np.array([159,50,230]), np.array([179,255,255]))
        red_mask = cv2.bitwise_or(red_mask1, red_mask2)
        
        blue_mask = cv2.inRange(hsv, np.array([100,50,240]), np.array([140,255,255]))

        blue_pts = cv2.findNonZero(blue_mask)
        red_pts = cv2.findNonZero(red_mask)

        if red_pts is not None:
            red_point = np.mean(red_pts, axis=(0, 1))
        else:
            red_point = None

        if blue_pts is not None:
            blue_point = np.mean(blue_pts, axis=(0, 1))
        else:
            blue_point = None

        return frame, red_point, blue_point

    def __iter__(self):
        return self




with BasicOpenCVPointReader() as pointReader:
    oldWindowSize = None
    cv2.namedWindow('video', cv2.WINDOW_KEEPRATIO)

    for frame, red, blue in pointReader:
        frame: cv2.Mat
        if red is not None:
            frame = cv2.circle(frame, (int(red[0]), int(red[1])), 10, (0, 0, 255), 2)
        if blue is not None:
            frame = cv2.circle(frame, (int(blue[0]), int(blue[1])), 10, (255, 0, 0), 2)

        cv2.imshow('video', frame)

        # Handle window resizing manually because at least on my Windows device OpenCV
        # is stupid and doesn't keep the image ratio on resize even though WINDOW_KEEPRATIO is set.
        curWindowSize = cv2.getWindowImageRect('video')[2:4]
        if oldWindowSize and curWindowSize != oldWindowSize:
            aspectRatio = (frame.shape[0] / frame.shape[1]) # rows / cols = y / w

            dw = abs(curWindowSize[0] - oldWindowSize[0])
            dy = abs(curWindowSize[1] - oldWindowSize[1])
            if dw > dy:
                w = curWindowSize[0]
                h = int(w * aspectRatio)
            else:
                h = curWindowSize[1]
                w = int(h / aspectRatio)
            cv2.resizeWindow('video', w, h)
            curWindowSize = (w, h)
        oldWindowSize = curWindowSize

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break