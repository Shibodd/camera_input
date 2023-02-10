import cv2
import numpy as np

class OpenCVError(Exception):
    '''An error caused by OpenCV'''
    pass

class BasicOpenCVPointReader:
    def __init__(self):
        self.green_min_range = np.array([0,0,145])
        self.green_max_range = np.array([255,115,255])
        self.red_min_range = np.array([0,145,160])
        self.red_max_range = np.array([255,255,255])

    def __enter__(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise OpenCVError("Errore durante l'apertura dell'obbiettivo")
            
        print("Camera running!") 
        return self

    def __exit__(self, *args):
        self.cap.release()
        self.cap = None
        print("Camera stopped!")

    def __next__(self):
        _, frame = self.cap.read()

        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        
        def process(min_range, max_range):
            im = cv2.inRange(lab, min_range,max_range)
            pts = cv2.findNonZero(im)
            if pts is not None:
                return np.mean(pts, axis=(0, 1))
            else:
                return None
        return (
            frame, 
            process(self.red_min_range, self.red_max_range),
            process(self.green_min_range, self.green_max_range)
        )

    def __iter__(self):
        return self


with BasicOpenCVPointReader() as pointReader:
    oldWindowSize = None
    cv2.namedWindow('video', cv2.WINDOW_KEEPRATIO)

    pointReader.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 352)
    pointReader.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)
    pointReader.cap.set(cv2.CAP_PROP_FPS, 60)

    for frame, red, green in pointReader:
        frame: cv2.Mat
        if red is not None:
            frame = cv2.circle(frame, (int(red[0]), int(red[1])), 10, (0, 0, 255), 2)
        if green is not None:
            frame = cv2.circle(frame, (int(green[0]), int(green[1])), 10, (0, 255, 0), 2)

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