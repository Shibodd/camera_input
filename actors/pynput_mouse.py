from pynput.mouse import Controller

class PynputMouseCursor:
    def __init__(self, pointSource, sensitivity = 1):
        self.mouse = Controller()
        self.pointSource = pointSource
        self.oldPt = None
        self.sensitivity = sensitivity
    
    def act(self):
        _, pt = next(self.pointSource)

        if pt is None:
            self.oldPt = None
            return

        if self.oldPt is not None:
            delta = (self.oldPt - pt) * self.sensitivity
        else:
            delta = None

        self.oldPt = pt
        
        if delta is not None:
            self.mouse.move(delta[0], delta[1])