import sys, logging
import config            
from direct.gui.DirectGui import *
import direct.directbase.DirectStart
from pandac.PandaModules import TextNode, ClockObject, Vec3
from direct.gui.OnscreenText import OnscreenText
from direct.showbase import DirectObject
from direct.showbase.DirectObject import DirectObject
from direct.task import Task
from direct.actor.Actor import Actor
from cameracontrol import CameraHandler
from tasks import FobPointUpdateTask, FobJointUpdateTask

class World(DirectObject):
    def __init__(self):
        self.escapeEventText = OnscreenText(text="ESC: Quit",
                                            fg=(1,1,1,1), pos=(-1.3, 0.95),
                                            align=TextNode.ALeft, scale=0.05)

        globalClock.setMode(ClockObject.MLimited)
        globalClock.setFrameRate(config.frame_rate)

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
#            taskMgr.add(MoveBoneTask(self.tinman), 'MoveBone')

            leftForearm = self.tinman.controlJoint(None, "modelRoot", "L_forearmBone")
            leftArm = self.tinman.controlJoint(None, "modelRoot", "L_armBone")

            taskMgr.add(FobJointUpdateTask(config.data_file, (leftArm, leftForearm)), 'FobJointUpdate')

            self.mainView = CameraHandler(base.camera, Vec3(40.576,-1.103,-4.825), Vec3(0,0,0))


def launch():        
    w = World()
    run()

if __name__ == "__main__":
    launch()
