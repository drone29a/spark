import direct.directbase.DirectStart
from pandac.PandaModules import TextNode, ClockObject, Vec3
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import OnscreenText
from direct.showbase import DirectObject
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.actor.Actor import Actor
import sys, logging
from cameracontrol import CameraHandler
from tasks import FobPointUpdateTask
import config

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

        self.tinman = Actor()
        self.tinman.loadModel("models/tinman")
        self.tinman.reparentTo(render)

        self.sensorNodes = [loader.loadModelCopy("models/planet_sphere") for i in range(3)]
        
        for sensorNode in self.sensorNodes:
            sensorNode.reparentTo(render)

        taskMgr.add(FobPointUpdateTask(config.data_file, 
                                       self.sensorNodes), 
                    'FobPointUpdate')

        class MoveBoneTask(object):
            def __init__(self, actor):
                self.actor = actor
                self.leftForearm = self.actor.controlJoint(None, "modelRoot", "L_forearmBone")

            def __call__(self, task):
                self.leftForearm.setHpr(20, 40, 30)

        taskMgr.add(MoveBoneTask(self.tinman), 'MoveBone')
        
        self.mainView = CameraHandler(base.camera, Vec3(40.576,-1.103,-4.825), Vec3(0,0,0))
            

def launch():        
    w = World()
    run()

if __name__ == "__main__":
    launch()
