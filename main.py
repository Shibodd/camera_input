import cv2
import numpy as np

import opencvsources as sources

with sources.OpenCVCameraFrameSource(0, cv2.CAP_DSHOW, 352, 288, 60) as cameraReader:
    pointReader = sources.BasicPointSource(cameraReader)

    oldWindowSize = None
    cv2.namedWindow('video', cv2.WINDOW_KEEPRATIO)

    for frame, red, green in pointReader:
        frame: cv2.Mat
        if red is not None:
            frame = cv2.circle(frame, (int(red[0]), int(red[1])), 10, (0, 0, 255), 2)
        if green is not None:
            frame = cv2.circle(frame, (int(green[0]), int(green[1])), 10, (0, 255, 0), 2)

        cv2.imshow('video', frame)

        # Handle window resizing manually because, at least on my Windows device,
        # OpenCV is stupid and doesn't keep the image ratio on resize even though WINDOW_KEEPRATIO is set.
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