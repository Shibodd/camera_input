import cv2
import numpy as np

import sources.opencvsources as sources
import processors.opencvprocessors as processors

with sources.OpenCVCameraFrameSource(0, cv2.CAP_DSHOW, 352, 288, 16) as camFrameSource:
    colConvFrameSource = processors.ColorConverterProcessor(camFrameSource, cv2.COLOR_BGR2LAB)

    greenPointReader = processors.SimpleColorRangePointProcessor(
        colConvFrameSource, [(
            np.array([0,   0, 145]),
            np.array([255, 115, 255])
        )])

    redPointReader = processors.SimpleColorRangePointProcessor(
        colConvFrameSource, [(
            np.array([0, 145, 160]),
            np.array([255, 255, 255])
        )])

    cv2.namedWindow('video', cv2.WINDOW_KEEPRATIO)

    for redResult, greenResult in zip(redPointReader, greenPointReader):
        nsR, red = redResult
        nsG, green = greenResult
        ns, frame = camFrameSource.get_last_frame()

        if red is not None:
            frame = cv2.circle(frame, (int(red[0]), int(red[1])), 10, (0, 0, 255), 2)
        if green is not None:
            frame = cv2.circle(frame, (int(green[0]), int(green[1])), 10, (0, 255, 0), 2)

        cv2.imshow('video', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break