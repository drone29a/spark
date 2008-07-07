from direct.task import Task
import utils
from itertools import izip, count
import config
from pandac.PandaModules import Vec3
from pandac.PandaModules import Quat

def segmentsFromMoment(moment):
    return [Vec3(*point2) - Vec3(*point1) for point1, point2 in zip(moment[:-1], moment[1:])]

def segmentsFromJoints(joints):
    return [Vec3(j2.getPos()) - Vec3(j1.getPos()) for j1, j2 in zip(joints[:-1], joints[1:])]

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
        self.prevSegmentVecs = segmentsFromJoints(self.joints)

    def __call__(self, task):
        for moment in self.dataStream:
            import logging
            for currSegmentVec, segmentVec, joint, endJoint in zip(self.prevSegmentVecs, segmentsFromMoment(moment), self.joints[:-1], self.joints[1:]):
                self.prevSegmentVecs.pop(0)

                currSegmentVec.normalize()
                segmentVec.normalize()

                axis = currSegmentVec.cross(segmentVec)
                axis.normalize()
                
                angle = currSegmentVec.angleRad(segmentVec)
                logging.debug("axis: %s, angle: %s" % (axis, angle))
                
                quat = Quat()
                quat.setFromAxisAngleRad(angle, axis)

                joint.setQuat(quat)

                self.prevSegmentVecs.append(segmentVec)
            return Task.cont
        return Task.done


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
                self.points[i].setPos(x, y, z)
            return Task.cont
        return Task.done
