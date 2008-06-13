import direct.directbase.DirectStart
from pandac.PandaModules import TextNode
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.showbase import DirectObject
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
import sys, logging

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

        self.accept('escape', sys.exit)
        base.disableMouse()
        base.setBackgroundColor(0, 0, 0, 0)
        base.textureOff()
        base.camera.setPos(0, 0, 200)
        base.camera.setHpr(0, -90, 0)

        self.sensorNodes = [loader.loadModelCopy("models/planet_sphere") for i in range(3)]
        
        for sensorNode in self.sensorNodes:
            sensorNode.reparentTo(render)
        
        debugText = OnscreenText(str(camera.getPos()), fg=(1,1,1,1),
                                 pos=(-1.3, 0.85), align=TextNode.ALeft, 
                                 scale=0.05, mayChange=True)
        debugText = OnscreenText(str(camera.getHpr()), fg=(1,1,1,1),
                                 pos=(-1.3, 0.75), align=TextNode.ALeft, 
                                 scale=0.05, mayChange=True)

        def trackShoulder(shoulderNode, task):
            base.camera.lookAt(shoulderNode)
            return Task.cont

        taskMgr.add(trackShoulder, 'TrackShoulder', extraArgs=[self.sensorNodes[0]], appendTask=True)
        taskMgr.add(FobPointUpdateTask('/Users/mrevelle/src/sparklemotion/data/fob/2008_06_09/001.dat'), 
                    'FobPointUpdate', extraArgs=[self.sensorNodes], appendTask=True)
            
        
w = World()
run()
