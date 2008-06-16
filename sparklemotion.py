import direct.directbase.DirectStart
from pandac.PandaModules import TextNode, ClockObject, Vec3
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.showbase import DirectObject
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
import sys, logging
from cameracontrol import CameraHandler
from fob import FobPointUpdateTask

class World(DirectObject):
    def __init__(self):
        self.escapeEventText = OnscreenText(text="ESC: Quit",
                                            fg=(1,1,1,1), pos=(-1.3, 0.95),
                                            align=TextNode.ALeft, scale=0.05)

        globalClock.setMode(ClockObject.MLimited)
        globalClock.setFrameRate(86.1)

        self.accept('escape', sys.exit)
        base.disableMouse()
        base.setBackgroundColor(0, 0, 0, 0)
        base.textureOff()
        base.setFrameRateMeter(True)

        self.sensorNodes = [loader.loadModelCopy("models/planet_sphere") for i in range(3)]
        
        for sensorNode in self.sensorNodes:
            sensorNode.reparentTo(render)

        taskMgr.add(FobPointUpdateTask('/Users/mrevelle/src/sparklemotion/data/fob/2008_06_09/001.dat', 
                                       self.sensorNodes), 
                    'FobPointUpdate')
        
        self.mainView = CameraHandler(base.camera, Vec3(40.576,-1.103,-4.825), Vec3(0,0,0))
            
        
w = World()
run()
