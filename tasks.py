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
        self.prevFobSegments = segmentsFromJoints(self.joints)
        self.prevJointSegments = segmentsFromJoints(self.joints)

    def __call__(self, task):
        for moment in self.dataStream:
            for prevSegment, segment, joint in zip(self.prevFobSegments, 
                                                             segmentsFromMoment(moment), 
                                                             self.joints[:-1]):
                self.prevFobSegments.pop(0)

                endJoint = joint.getChild(0)

                prevJointSegment = Vec3(endJoint.getNetTransform().getPos()) - Vec3(joint.getNetTransform().getPos())
                prevJointSegment.setZ(-prevJointSegment.getZ())

                prevSegment.normalize()
                segment.normalize()
                prevJointSegment.normalize()

                axis = prevSegment.cross(segment)
                axis.normalize()

                import logging
                logging.debug("moment: %s" % (moment,))
                logging.debug("segment: %s, prevSegment: %s, prevJointSegment: %s" % (segment, prevSegment, prevJointSegment))
                logging.debug("axis: %s" % (axis,))
                
                angle = prevSegment.angleRad(segment)

                quat = Quat()
                quat.setFromAxisAngleRad(angle, axis)

                joint.setQuat(joint, quat)

                self.prevFobSegments.append(segment)
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
