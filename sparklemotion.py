import direct.directbase.DirectStart
from pandac.PandaModules import TextNode, ClockObject, Vec3
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.showbase import DirectObject
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
import sys, logging
from cameracontrol import CameraHandler

class FobPointUpdateTask(object):
    def __init__(self, filePath):
        self.filePath = filePath
        self.f = open(filePath, 'r')

    def __lines(self, num):
        result = []
        for i in range(num):
            result.append(self.f.readline())
        return result

    def __call__(self, points, task):
        newPositions = [[float(val) for val in line.split()[1:4]] for line in self.__lines(3)]
        if len(newPositions[0]) is 0:
            self.f.close()
            return Task.done
        
        for i in range(3):
            points[i].setPos(*newPositions[i])
            
        return Task.cont

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

        def trackShoulder(shoulderNode, task):
            base.camera.lookAt(shoulderNode)
            return Task.cont

#        taskMgr.add(trackShoulder, 'TrackShoulder', extraArgs=[self.sensorNodes[0]], appendTask=True)
        taskMgr.add(FobPointUpdateTask('/Users/mrevelle/src/sparklemotion/data/fob/2008_06_09/001.dat'), 
                    'FobPointUpdate', extraArgs=[self.sensorNodes], appendTask=True)

        self.testNode = loader.loadModelCopy("models/planet_sphere")
        self.testNode.reparentTo(render)
        self.testHandler = CameraHandler(self.testNode, self.sensorNodes[0].getPos(), Vec3(-90,0,90))
        base.camera.setPos(400,0,0)
        base.camera.lookAt(self.sensorNodes[0])
        base.camera.setR(90)
        
#        self.mainView = CameraHandler(base.camera, self.sensorNodes[0].getPos(), Vec3(0,90,0))
#        base.camera.lookAt(self.sensorNodes[0])
            
        
w = World()
run()
