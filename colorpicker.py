import cv2
import numpy as np
from sources.opencvsources import OpenCVCameraFrameSource

def nothing(x):
    pass

with OpenCVCameraFrameSource(0, cv2.CAP_DSHOW, 352, 288, 16) as cam:
    # Create a window
    cv2.namedWindow('image')

    CONV = cv2.COLOR_BGR2HSV
    channels = [
        ('H', 0, 180),
        ('S', 0, 255),
        ('V', 0, 255),
    ]

    for ch in channels:
        cv2.createTrackbar(f'{ch[0]}Min', 'image', ch[1], ch[2], nothing)
        cv2.createTrackbar(f'{ch[0]}Max', 'image', ch[1], ch[2], nothing)
        cv2.setTrackbarPos(f'{ch[0]}Max', 'image', ch[2])

    while True:
        _, image = cam.tick()

        mins = [cv2.getTrackbarPos(f'{ch[0]}Min', 'image') for ch in channels]
        maxs = [cv2.getTrackbarPos(f'{ch[0]}Max', 'image') for ch in channels]

        lower = np.array(mins)
        upper = np.array(maxs)

        hsv = cv2.cvtColor(image, CONV)
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(image, image, mask=mask)

        cv2.imshow('image', result)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()
