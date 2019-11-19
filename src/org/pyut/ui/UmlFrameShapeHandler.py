
from logging import Logger
from logging import getLogger

from wx import Window

from MiniOgl.DiagramFrame import DiagramFrame
from org.pyut.PyutActor import PyutActor
from org.pyut.PyutClass import PyutClass
from org.pyut.PyutNote import PyutNote
from org.pyut.PyutUseCase import PyutUseCase
from org.pyut.ogl.OglActor import OglActor
from org.pyut.ogl.OglClass import OglClass

from org.pyut.general.Globals import _
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglUseCase import OglUseCase


class UmlFrameShapeHandler(DiagramFrame):

    def __init__(self, parent: Window):

        super().__init__(parent)

        self.logger: Logger = getLogger(__name__)

    def createNewClass(self, x, y):
        """
        Add a new class at (x, y).

        @return PyutClass : the newly created PyutClass
        """
        pyutClass: PyutClass = PyutClass(_("NoName"))
        oglClass:  OglClass  = OglClass(pyutClass)

        self.addShape(oglClass, x, y)
        self.Refresh()
        return pyutClass

    def createNewNote(self, x, y):
        """
        Add a new note at (x, y).

        @return PyutNote : the newly created PyutNote
        """
        pyutNote: PyutNote = PyutNote("")
        oglNote:  OglNote  = OglNote(pyutNote)

        self.addShape(oglNote, x, y)
        self.Refresh()
        return pyutNote

    def createNewActor(self, x, y):
        """
        Add a new actor at (x, y).

        @return PyutActor : the newly created PyutActor
        """
        pyutActor: PyutActor = PyutActor()
        oglActor:  OglActor  = OglActor(pyutActor)

        self.addShape(oglActor, x, y)
        self.Refresh()
        return pyutActor

    def createNewUseCase(self, x, y):
        """
        Add a new use case at (x, y).

        @return PyutUseCase : the newly created PyutUseCase
        """
        pyutUseCase: PyutUseCase = PyutUseCase()
        oglUseCase:  OglUseCase  = OglUseCase(pyutUseCase)

        self.addShape(oglUseCase, x, y)
        self.Refresh()
        return pyutUseCase

    def addShape(self, shape, x, y, pen=None, brush=None, withModelUpdate=True):
        """
        Add a shape to the UmlFrame.

        @param wx.Shape shape : the shape to add
        @param int x : coord of the center of the shape
        @param int y : coord of the center of the shape
        @param wx.Pen pen : pen to use
        @param wx.Brush brush : brush to use
        @param withModelUpdate  :   if true the model of the shape will
                                            update from the shape (view) when
                                            added to the diagram. Added by
                                            P. Dabrowski (29.11.05)
        @since 1.4
        @author L. Burgbacher <lb@alawa.ch>
        """
        shape.SetDraggable(True)
        shape.SetPosition(x, y)
        if pen:
            shape.SetPen(pen)
        if brush:
            shape.SetBrush(brush)
        self._diagram.AddShape(shape, withModelUpdate)

