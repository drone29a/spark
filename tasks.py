from direct.task import Task
import utils
from itertools import izip, count
import config
from pandac.PandaModules import Vec3
from pandac.PandaModules import Quat

def segmentsFromMoment(moment):
    return [Vec3(*point2) - Vec3(*point1) for point1, point2 in zip(moment[:-1], moment[1:])]

def segmentsFromJoints(startJoints, endJoints):
    return [Vec3(j2.getPos()) - Vec3(j1.getPos()) for j1, j2 in zip(startJoints, endJoints)]

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
    def __init__(self, filePath, actor, joints):
        """
        filePath - path to file of FoB data
        joints - collection of joints, ordered by heaviness
        """
        self.filePath = filePath
        self.actor = actor
        self.joints = joints
        self.controlJoints = [self.actor.controlJoint(None, "modelRoot", joint) for joint in self.joints]
        self.exposedJoints = [self.actor.exposeJoint(None, "modelRoot", joint) for joint in self.joints]
        self.data = utils.readData(filePath, config.num_sensors)
        self.dataStream = izip(*self.data)
        self.prevFobSegments = segmentsFromJoints(self.exposedJoints[:-1], self.exposedJoints[1:])
        self.prevJointSegments = segmentsFromJoints(self.exposedJoints[:-1], self.exposedJoints[1:])
        self.stopped = False
        self.paused = False

    def __call__(self, task):
        for moment in self.dataStream:
            for prevSegment, segment, controlJoint, jointName, endJointName in zip(self.prevFobSegments, 
                                                                                   segmentsFromMoment(moment), 
                                                                                   self.controlJoints[:-1],
                                                                                   self.joints[:-1],
                                                                                   self.joints[1:]):
                while self.paused:
                    return Task.cont

                self.prevFobSegments.pop(0)
                
                exposedJoint = self.actor.exposeJoint(None, "modelRoot", jointName)
                exposedEndJoint = self.actor.exposeJoint(None, "modelRoot", endJointName)
                prevJointSegment = Vec3(exposedEndJoint.getNetTransform().getPos()) - Vec3(exposedJoint.getNetTransform().getPos())

                prevSegment.normalize()
                segment.normalize()
                prevJointSegment.normalize()

                axis = prevJointSegment.cross(segment)
                axis.normalize()

                import logging
#                logging.debug("moment: %s" % (moment,))
#                logging.debug("segment: %s, prevSegment: %s, prevJointSegment: %s" % (segment, prevSegment, prevJointSegment))
#                logging.debug("prevJointSegment: %s" % (prevJointSegment,))
#                logging.debug("axis: %s" % (axis,))
                
                angle = prevSegment.angleRad(segment)

                quat = Quat()
                quat.setFromAxisAngleRad(angle, axis)

                controlJoint.setQuat(controlJoint, quat)

                self.prevFobSegments.append(segment)
            if not self.stopped:
                return Task.cont
            else:
                return Task.done
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
