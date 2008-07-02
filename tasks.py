from direct.task import Task
import utils
from itertools import izip, count
import config
from pandac.PandaModules import Vec3
from pandac.PandaModules import Quat

def getQuat(x1,y1,z1,x2,y2,z2):
	"""Calculate the quaternion which rotates between one vector and another.
	"""

	# initialize vectors
	v1 = Vec3(x1, y1, z1)
	v2 = Vec3(x2, y2, z2)

	# get axis
	axis = v1.cross(v2)
	axis.normalize()

	# get angle
	angle = v1.angleRad(v2)

	# make quaternion (from axis/angle representation)
	quat = Quat()
	quat.setFromAxisAngleRad(angle,axis)

	# return Panda3d quaternion representing motion between two vectors
	return quat

def segmentsFromMoment(moment):
    return [Vec3(*point2) - Vec3(*point1) for point1 in moment for point2 in moment[1:]][:-1]

class MoveBoneTask(object):
    def __init__(self, actor):
        self.actor = actor
        self.leftForearm = self.actor.controlJoint(None, "modelRoot", "L_forearmBone")
        
    def __call__(self, task):
        self.leftForearm.setHpr(20, 40, 30)

class FobJointUpdateTask(object):
    """
    Task for animating joints from FoB data.
    """
    def __init__(self, filePath, joints):
        """
        filePath - path to file of FoB data
        joints - collection of joints, ordered by heaviness
        """
        self.filePath = filePath
        self.joints = joints
        self.data = utils.readData(filePath, config.num_sensors)
        self.dataStream = izip(*self.data)
        self.segments = [None, None]  # Current state of limb segments

    def __call__(self, task):
        for moment in self.dataStream:
            for prevSegmentVect, segmentVect, joint in zip(self.segments, segmentsFromMoment(moment), self.joints):
                if prevSegmentVect is None:
                    break
                
                axis = prevSegmentVect.cross(segmentVect)
                axis.normalize()
                
                angle = prevSegmentVect.angleRad(segmentVect)
                
                quat = Quat()
                quat.setFromAxisAngleRad(angle, axis)

                joint.setQuat(quat)

            self.segments = segmentsFromMoment(moment)
            return Task.cont
        return Task.stop


class FobPointUpdateTask(object):
    """
    Task for updating a position of points from FoB data.
    """
    def __init__(self, filePath, points):
        self.filePath = filePath
        self.data = utils.readData(filePath, config.num_sensors)
        self.points = points
        self.dataStream = izip(*self.data)

    def __call__(self, task):
        for moments in self.dataStream:
            for i in range(config.num_sensors):
                (x, y, z) = moments[i]
                z = -z
                self.points[i].setPos(x, y, z)
            return Task.cont
        return Task.done
