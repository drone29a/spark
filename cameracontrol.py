from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import Point3D, Vec3

class CameraHandler(DirectObject):
    class DIRECTION(object):
        UP = 0
        DOWN = 1
        LEFT = 2
        RIGHT = 3

    __nextId = 0

    @classmethod
    def requestId(cls):
        """
        Returns the next valid id, each CameraHandler has an associated
        id to avoid name clashes.
        """
        id = cls.__nextId
        cls.__nextId += 1
        return id

    def __init__(self, camera, pos=Point3D(0,0,0), orientation=Vec3(0,0,0), keymap=None):
        """
        Inits a handler for a camera and uses the given keymap to setup event handling.
        """
        self.camera = camera
        self.id = CameraHandler.requestId()
        self.focalPoint = render.attachNewNode("focalPoint%s" % self.id)
        self.focalPoint.setPos(pos)
        self.focalPoint.setHpr(orientation)
        self.camera.reparentTo(self.focalPoint)
        self.camera.setPos(100, 0, 0)
        self.camera.lookAt(self.focalPoint)
        self.camera.setHpr(orientation)

        self.accept("arrow_left", self.orbit, extraArgs=[CameraHandler.DIRECTION.LEFT])
        self.accept("arrow_left-repeat", self.orbit, extraArgs=[CameraHandler.DIRECTION.LEFT])
        self.accept("arrow_right", self.orbit, extraArgs=[CameraHandler.DIRECTION.RIGHT])
        self.accept("arrow_right-repeat", self.orbit, extraArgs=[CameraHandler.DIRECTION.RIGHT])

        self.accept("arrow_up", self.zoom, extraArgs=[CameraHandler.DIRECTION.UP])
        self.accept("arrow_up-repeat", self.zoom, extraArgs=[CameraHandler.DIRECTION.UP])
        self.accept("arrow_down", self.zoom, extraArgs=[CameraHandler.DIRECTION.DOWN])
        self.accept("arrow_down-repeat", self.zoom, extraArgs=[CameraHandler.DIRECTION.DOWN])

    def orbit(self, direction):
        """
        Slide the camera in the left or right direction (CameraHandler.{LEFT, RIGHT}).
        """
        if direction is CameraHandler.DIRECTION.LEFT:
            self.focalPoint.setH(self.focalPoint, 5)
        elif direction is CameraHandler.DIRECTION.RIGHT:
            self.focalPoint.setH(self.focalPoint, -5)

        self.camera.lookAt(self.focalPoint)
        self.camera.setHpr(self.focalPoint.getHpr())

    def zoom(self, direction):
        """
        Zoom in and out by translating camera towards/away focal point.
        """
        if direction is CameraHandler.DIRECTION.UP:
            self.camera.setZ(self.camera, 10)
        elif direction is CameraHandler.DIRECTION.DOWN:
            self.camera.setZ(self.camera, -10)
