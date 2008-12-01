import sys, os, logging
import config            
from direct.gui.DirectGui import *
from pandac.PandaModules import TextNode, ClockObject, Vec3, Vec4, WindowProperties, DirectionalLight, AmbientLight, loadPrcFileData
loadPrcFileData("", "fullscreen 1")
import direct.directbase.DirectStart
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
    def _resetTinman(self):
        pos = self.tinman.getPos()
        self.tinman.detachNode()
        self.tinman = Actor()
        self.tinman.loadModel("models/tinman")
        self.tinman.reparentTo(render)
        self.tinman.setScale(1.35)
        self.tinman.setColor(0, 1, 0)
        self.tinman.setPos(pos)

    def _restartFob(self, dataFile):
        if self.fobTask:
            self.fobTask.stopped = True
            taskMgr.remove('FobJointUpdate')

        self._resetTinman()

        self.fobTask = FobJointUpdateTask(dataFile, self.tinman, ("L_armBone", "L_forearmBone", "L_wristBone"))
        taskMgr.add(self.fobTask, 'FobJointUpdate')

    def _togglePauseFob(self):
        self.fobTask.paused = not self.fobTask.paused

    def __init__(self):
        wp = WindowProperties() 
        wp.setTitle('Sparkle') 
        base.win.requestProperties(wp)

#         self.escapeEventText = OnscreenText(text="ESC: Quit",
#                                             fg=(1,1,1,1), pos=(-1.3, 0.95),
#                                             align=TextNode.ALeft, scale=0.05)

        globalClock.setMode(ClockObject.MLimited)
        globalClock.setFrameRate(config.frame_rate)

        self.accept('escape', sys.exit)
        self.accept('control-s', base.screenshot)
        base.disableMouse()
        base.setBackgroundColor(0, 0, 0, 0)
        base.textureOff()
        base.setFrameRateMeter(True)

        self.accept('1', self._restartFob, [config.dataFiles[0]])
        self.accept('2', self._restartFob, [config.dataFiles[1]])
        self.accept('3', self._restartFob, [config.dataFiles[2]])
        self.accept('space', self._togglePauseFob)
        
        self.tinman = Actor()
        self.tinman.loadModel("models/tinman")
        self.tinman.reparentTo(render)
        self.tinman.setScale(1.35)
        self.tinman.setColor(0, 1, 0)
        
        # Init tinman's position and pose
        rootBone = self.tinman.exposeJoint(None, "modelRoot", "RootBone")
        leftArm = self.tinman.exposeJoint(None, "modelRoot", "L_armBone")
            
        fobData = readData(config.data_file, config.num_sensors)
        shoulderInitPos = Vec3(*fobData[0][0])
        self.tinman.setPos(shoulderInitPos - leftArm.getPos())

        dlight = DirectionalLight('dlight')
        dlightNode = self.tinman.attachNewNode(dlight)
        dlightNode.setPos(Vec3(100, -200, 50))
        dlightNode.lookAt(self.tinman)
        render.setLight(dlightNode)

        alight = AmbientLight('alight')
        alight.setColor(Vec4(0.2, 0.2, 0.2, 1))
        alightNode = self.tinman.attachNewNode(alight)
        alightNode.setPos(Vec3(0, 200, 100))
        render.setLight(alightNode)

#         self.sensorNodes = [loader.loadModelCopy("models/planet_sphere") for i in range(3)]
        
#         for sensorNode in self.sensorNodes:
#             sensorNode.reparentTo(render)

#         taskMgr.add(FobPointUpdateTask(config.data_file, 
#                                        self.sensorNodes), 
#                     'FobPointUpdate')
        
        self.fobTask = FobJointUpdateTask(config.data_file, self.tinman, ("L_armBone", "L_forearmBone", "L_wristBone"))
        taskMgr.add(self.fobTask, 'FobJointUpdate')
        
        self.mainView = CameraHandler(base.camera, Vec3(40.576,-1.103,-4.825), Vec3(0,0,0))

def launch():        
    w = World()
    run()

if __name__ == "__main__":
    launch()
