import sys, os, logging
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
from utils import readData

logging.basicConfig(filename=os.path.join(config.prog_path, "out.log"), level=logging.DEBUG)
logging.debug("STARTING")

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
        
        # Init tinman's position and pose
        rootBone = self.tinman.exposeJoint(None, "modelRoot", "RootBone")
        leftArm = self.tinman.exposeJoint(None, "modelRoot", "L_armBone")
            
        fobData = readData(config.data_file, config.num_sensors)
        shoulderInitPos = Vec3(*fobData[0][0])
        self.tinman.setPos(shoulderInitPos - leftArm.getPos())

        self.sensorNodes = [loader.loadModelCopy("models/planet_sphere") for i in range(3)]
        
        for sensorNode in self.sensorNodes:
            sensorNode.reparentTo(render)

        taskMgr.add(FobPointUpdateTask(config.data_file, 
                                       self.sensorNodes), 
                    'FobPointUpdate')
 
        taskMgr.add(FobJointUpdateTask(config.data_file, self.tinman, ("L_armBone", "L_forearmBone", "L_wristBone")), 'FobJointUpdate')
        
        self.mainView = CameraHandler(base.camera, Vec3(40.576,-1.103,-4.825), Vec3(0,0,0))


def launch():        
    w = World()
    run()

if __name__ == "__main__":
    launch()
