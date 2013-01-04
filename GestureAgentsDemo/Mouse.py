from GestureAgentsTUIO.Tuio import TuioAgentGenerator
from pyglet.window import mouse

class MouseAsTuioAgentGenerator(object):
    """docstring for MouseAsTuioAgentGenerator"""
    def __init__(self):
        self.pressed = False
        self.myagent = None
        self.sid = -1
    def on_mouse_press(self,x, y, button, modifiers):
        if button == mouse.LEFT:
            self.pressed = True
            self.myagent = TuioAgentGenerator.makeCursorAgent()
            self._updateAgent(self.myagent,(x,y))
            self.myagent.newAgent(self.myagent)
            self.myagent.newCursor(self.myagent)
    def on_mouse_release(self,x, y, button, modifiers):
        if button == mouse.LEFT:
            self.pressed = False
            self._updateAgent(self.myagent,(x,y))
            self.myagent.removeCursor(self.myagent)
            self.myagent.finish()
            self.myagent = None
    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            self._updateAgent(self.myagent,(x,y))
            self.myagent.updateCursor(self.myagent)
    
    def _updateAgent(self,a,pos):
        a.pos = pos
        a.posx = pos[0]
        a.posy = pos[1]
        a.sessionid = self.sid
        a.xmot = 0
        a.ymot = 0
        a.mot_accel = 0