import cv2
import numpy as np

import sources.opencvsources as sources
import processors.opencvprocessors as processors
from pipeline import Pipeline
from actors.protractor import Protractor
from actors.frame_point_renderer import FramePointRenderer

camFrameSource = sources.OpenCVCameraFrameSource(0, cv2.CAP_ANY, 352, 288, 30)
blurredFrameSource = processors.BlurProcessor(camFrameSource, 5)
colConvFrameSource = processors.ColorConverterProcessor(blurredFrameSource, cv2.COLOR_BGR2HSV)

greenPointReader = processors.SimpleColorRangePointProcessor(
    colConvFrameSource, [
        (np.array([64, 215, 126]), np.array([89, 255, 255])) 
    ])

redPointReader = processors.SimpleColorRangePointProcessor(
    colConvFrameSource, [
        ( np.array([0,   180, 150]), np.array([20,  255,255]) ),
        ( np.array([130, 180, 150]), np.array([180, 255, 255]) )
    ])

protractor = Protractor(redPointReader, greenPointReader)
dbg_rend = FramePointRenderer(blurredFrameSource, [
    (redPointReader, (0, 0, 255)), 
    (greenPointReader, (0, 255, 0))
])

pipeline = Pipeline(camFrameSource)
pipeline.add_actor(protractor)
pipeline.add_actor(dbg_rend)

with camFrameSource, protractor, dbg_rend:
    while True:
        pipeline.tick()
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break