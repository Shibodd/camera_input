import cv2
import typing

class FramePointRenderer:
    def __init__(self, frameSource, pointSources: typing.Iterable[typing.Tuple]):
        self.pointSources = pointSources
        self.frameSource = frameSource

    def __enter__(self):
        cv2.namedWindow(str(id(self)))
        cv2.setWindowTitle(str(id(self)), "Frame Point Renderer")
        return self
    def __exit__(self, *args):
        cv2.destroyWindow(str(id(self)))

    def act(self):
        _, frame = next(self.frameSource)
        for pointSource, color in self.pointSources:
            _, pt = next(pointSource)
            if pt is not None:
                frame = cv2.circle(frame, (int(pt[0]), int(pt[1])), 10, color, 2)

        cv2.imshow(str(id(self)), frame)