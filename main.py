import cv2
import numpy as np

import sources.opencvsources as sources
import processors.opencvprocessors as cv_processors
import processors.processors as processors
from pipeline import Pipeline
from actors.protractor import Protractor
from actors.frame_point_renderer import FramePointRenderer
from actors.pynput_mouse import PynputMouseCursor


camFrameSource = sources.OpenCVCameraFrameSource(0, cv2.CAP_DSHOW, 352, 288, 16)
blurredFrameSource = cv_processors.BlurProcessor(camFrameSource, 3, 3)
colConvFrameSource = cv_processors.ColorConverterProcessor(blurredFrameSource, cv2.COLOR_BGR2HSV)

greenPointProcessor = cv_processors.SimpleColorRangePointProcessor(
    colConvFrameSource, [
        #(np.array([64, 215, 126]), np.array([89, 255, 255])) 
        ( np.array([40, 118, 180]), np.array([53,255, 255]) )
    ])

redPointProcessor = cv_processors.SimpleColorRangePointProcessor(
    colConvFrameSource, [
        ( np.array([0,   180, 150]), np.array([20,  255,255]) ),
        ( np.array([130, 180, 150]), np.array([180, 255, 255]) )
    ])


armPointProcessor = processors.ArmProcessor(redPointProcessor, greenPointProcessor, 0)

protractor = Protractor(redPointProcessor, greenPointProcessor)
dbg_rend = FramePointRenderer(camFrameSource, [
    (redPointProcessor, (0, 0, 255)), 
    (greenPointProcessor, (0, 255, 0)),
    (armPointProcessor, (255, 255, 255))
])
mouse = PynputMouseCursor(armPointProcessor, 10)

pipeline = Pipeline(camFrameSource, protractor, dbg_rend, mouse)

with camFrameSource, protractor, dbg_rend:
    while True:
        pipeline.tick()
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break