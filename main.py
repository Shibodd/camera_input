import cv2
import numpy as np

import sources.opencvsources as sources
import processors.opencvprocessors as processors
from pipeline import Pipeline
from actors.protractor import Protractor
from actors.frame_point_renderer import FramePointRenderer
from actors.pynput_mouse import PynputMouseCursor


camFrameSource = sources.OpenCVCameraFrameSource(0, cv2.CAP_DSHOW, 352, 288, 16)
blurredFrameSource = processors.BlurProcessor(camFrameSource, 3, 3)
colConvFrameSource = processors.ColorConverterProcessor(blurredFrameSource, cv2.COLOR_BGR2HSV)

greenPointReader = processors.SimpleColorRangePointProcessor(
    colConvFrameSource, [
        #(np.array([64, 215, 126]), np.array([89, 255, 255])) 
        ( np.array([40, 118, 180]), np.array([53,255, 255]) )
    ])

redPointReader = processors.SimpleColorRangePointProcessor(
    colConvFrameSource, [
        ( np.array([0,   180, 150]), np.array([20,  255,255]) ),
        ( np.array([130, 180, 150]), np.array([180, 255, 255]) )
    ])

protractor = Protractor(redPointReader, greenPointReader)
dbg_rend = FramePointRenderer(camFrameSource, [
    (redPointReader, (0, 0, 255)), 
    (greenPointReader, (0, 255, 0))
])

mouse = PynputMouseCursor(redPointReader, 10)

pipeline = Pipeline(camFrameSource)
pipeline.add_actor(protractor)
pipeline.add_actor(dbg_rend)
pipeline.add_actor(mouse)

with camFrameSource, protractor, dbg_rend:
    while True:
        pipeline.tick()
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break