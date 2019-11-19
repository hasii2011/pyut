
from typing import List
from typing import Dict

from logging import Logger
from logging import getLogger

from wx import BeginBusyCursor
from wx import EVT_CHAR
from wx import EVT_CLOSE
from wx import EVT_PAINT
from wx import EndBusyCursor
from wx import MouseEvent

from org.pyut.PyutClass import PyutClass
from org.pyut.PyutActor import PyutActor
from org.pyut.PyutUseCase import PyutUseCase
from org.pyut.PyutMethod import PyutMethod

from org.pyut.PyutNote import PyutNote

from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglActor import OglActor
from org.pyut.ogl.OglUseCase import OglUseCase
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglLink import OglLink
from OglSDMessage import OglSDMessage

from MiniOgl.Constants import SKIP_EVENT
from MiniOgl.DiagramFrame import DiagramFrame

from Mediator import ACTION_ZOOM_IN
from Mediator import getMediator

from org.pyut.PyutUtils import PyutUtils

from org.pyut.history.HistoryManager import HistoryManager

from org.pyut.general.Globals import _

#  DEFAULT_WIDTH = 1280
#  DEFAULT_WIDTH = 5120

DEFAULT_WIDTH = 3000


class UmlFrame(DiagramFrame):
    """
    Represents a canvas for drawing diagrams.
    It provides all the methods to add new classes, notes, links...
    It also routes some click events to the mediator. See the `OnLeftDown`
    method.

    :version: $Revision: 1.22 $
    :author: L. Burgbacher
    :contact: lb@alawa.ch
    """
    def __init__(self, parent, frame):
        """
        constructor
        @param wx.Window parent : parent object
        @param frame : parent frame object
        @since 1.0
        @author N. hamadi (hamadi12@yahoo.fr)
        @modified L. Burgbacher <lb@alawa.ch>
            added event processing
            added mediator support
            bind with OglClass to create new classes
        """

        super().__init__(parent)

        self.logger: Logger = getLogger(__name__)

        self._ctrl = getMediator()
        self.maxWidth  = DEFAULT_WIDTH
        self.maxHeight = int(self.maxWidth / 1.41)  # 1.41 is for A4 support

        # set a scrollbar
        self.SetScrollbars(20, 20, self.maxWidth/20, self.maxHeight/20)

        self._frame = frame
        self._history = HistoryManager(self)

        # Close event
        self.Bind(EVT_CLOSE, self.evtClose)
        self.Bind(EVT_PAINT, self.OnPaint)
        self.Bind(EVT_CHAR, self._ctrl.processChar)

        self.SetInfinite(True)

        self._defaultCursor = self.GetCursor()

    def setCodePath(self, path):
        """
        Set the code path
        DEPRECATED
        @author C.Dutoit
        """
        project = self._ctrl.getFileHandling().getProjectFromFrame(self)
        if project is not None:
            project.setCodePath(path)
        else:
            print("Passing setCodePath in UmlFrame-setCodePath")

    def displayDiagramProperties(self):
        """
        Display class diagram properties
        @author C.Dutoit
        """
        PyutUtils.displayError(_("Not yet implemented !"))

    def cleanUp(self):
        """
        Clean up object references before quitting.

        @since 1.23
        @author Laurent Burgbacher <lb@alawa.ch>
        @modified C.Dutoit <dutoitc@hotmail.com>
            Added clean destroy code
        """
        self._ctrl = None
        self._frame = None

    # noinspection PyUnusedLocal
    def evtClose(self, event):
        """
        Clean close, event handler on EVT_CLOSE

        @since 1.35.2.8
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        self._history.destroy()

        self.cleanUp()
        self.Destroy()

    def newDiagram(self):
        """
        Remove all shapes, get a brand new empty diagram.

        @since 1.31
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self._diagram.DeleteAllShapes()
        self.Refresh()

    def getDiagram(self):
        """
        Return the diagram of this frame.

        @return wx.Diagram
        @since 1.23
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self._diagram

    def addHierarchy(self, display):
        """
        Hardcoded example of a class diagram, for test purposes.
        Classes come from self introspection !!!
        OK, it's too big, but it's not a feature, just a toy.

        @author L. Burgbacher <lb@alawa.ch>
        @since 1.4
        """
        BeginBusyCursor()

        from org.pyut.experimental.ClassGenerator import ClassGenerator
        from org.pyut.experimental.AddHierarchy import AddHierarchy

        cg: ClassGenerator = ClassGenerator()
        classes: List[type] = cg.getClassListFromNames(display)

        classNameToOglClass: Dict[str, OglClass] = {}

        addHierarchy: AddHierarchy = AddHierarchy(umlFrame=self, maxWidth=self.maxWidth, historyManager=self._history)
        # create the Pyut Class objects & associate Ogl graphical classes
        for cl in classes:
            # create objects
            pyutClassDef: PyutClass = PyutClass(cl.__name__)

            clmethods: List[classmethod] = cg.getMethodsFromClass(cl)

            # add the methods
            methods: List[PyutMethod] = cg.generatePyutMethods(clmethods)
            methods = sorted(methods, key=PyutMethod.getName)

            pyutClassDef.setMethods(methods)

            oglClassDef = addHierarchy.addToDiagram(pyutClassDef)
            classNameToOglClass[cl.__name__] = oglClassDef

        # now, search for parent links
        for oglClassDef in classNameToOglClass.values():

            pyutClassDef = oglClassDef.getPyutObject()
            # skip object, it has no parent
            if pyutClassDef.getName() == "object":
                continue

            parentNames = cg.getParentClassNames(classes, pyutClassDef)

            for parent in parentNames:
                dest = classNameToOglClass.get(parent)
                if dest is not None:  # maybe we don't have the parent loaded
                    addHierarchy.createInheritanceLink(oglClassDef, dest)

        oglClassDefinitions: List[OglClass] = list(classNameToOglClass.values())

        addHierarchy.positionClassHierarchy(oglClassDefinitions)

        EndBusyCursor()

    def addPyutHierarchy(self):
        """
        Calls AddHierarchy with the Pyut classes list.

        @since 1.32
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        import PyutDataClasses as pdc
        self.addHierarchy(pdc.display)

    def addOglHierarchy(self):
        """
        Calls AddHierarchy with the Ogl classes list.

        @since 1.32
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        import PyutDataClasses as pdc
        self.addHierarchy(pdc.displayOgl)

    def createNewClass(self, x, y):
        """
        Add a new class at (x, y).

        @return PyutClass : the newly created PyutClass
        @since 1.4
        @author L. Burgbacher <lb@alawa.ch>
        """
        pyutClass = PyutClass(_("NoName"))
        oglClass = OglClass(pyutClass)
        self.addShape(oglClass, x, y)
        self.Refresh()
        return pyutClass

    def createNewNote(self, x, y):
        """
        Add a new note at (x, y).

        @return PyutNote : the newly created PyutNote
        @since 1.35.2.2
        @author P. Waelti <pwaelti@eivd.ch>
        """
        pyutNote = PyutNote("")
        oglNote = OglNote(pyutNote)
        self.addShape(oglNote, x, y)
        self.Refresh()
        return pyutNote

    def createNewActor(self, x, y):
        """
        Add a new actor at (x, y).

        @return PyutActor : the newly created PyutActor
        @since 1.35.2.4
        @author P. Waelti <pwaelti@eivd.ch>
        """
        pyutActor = PyutActor()
        oglActor = OglActor(pyutActor)
        self.addShape(oglActor, x, y)
        self.Refresh()
        return pyutActor

    def createNewUseCase(self, x, y):
        """
        Add a new use case at (x, y).

        @return PyutUseCase : the newly created PyutUseCase
        @since 1.35.2.4
        @author P. Waelti <pwaelti@eivd.ch>
        """
        pyutUseCase = PyutUseCase()
        oglUseCase = OglUseCase(pyutUseCase)
        self.addShape(oglUseCase, x, y)
        self.Refresh()
        return pyutUseCase

    def OnLeftDown(self, event):
        """
        Manage a left down mouse event.
        If there's an action pending in the mediator, give it the event, else
        let it go to the next handler.

        @param  event
        @since 1.4
        @author L. Burgbacher <lb@alawa.ch>
        """

        if self._ctrl.actionWaiting():
            x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
            skip = self._ctrl.doAction(x, y)

            if self._ctrl.getCurrentAction() == ACTION_ZOOM_IN:
                DiagramFrame._BeginSelect(self, event)

            if skip == SKIP_EVENT:
                DiagramFrame.OnLeftDown(self, event)

        else:
            DiagramFrame.OnLeftDown(self, event)

    def OnLeftUp(self, event):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (11.11.2005)
        to make the right action if it is a selection or a zoom.
        """
        if self._ctrl.getCurrentAction() == ACTION_ZOOM_IN:
            width, height = self._selector.GetSize()
            x, y = self._selector.GetPosition()
            self._selector.Detach()
            self._selector = None
            self.DoZoomIn(x, y, width, height)
            self.Refresh()
            self._ctrl.updateTitle()
        else:

            DiagramFrame.OnLeftUp(self, event)

    def OnLeftDClick(self, event: MouseEvent):
        """
        Manage a left double click mouse event.

        @param  event
        @since 1.22
        @author L. Burgbacher <lb@alawa.ch>
        """
        x, y = self.CalcUnscrolledPosition(event.GetX(), event.GetY())
        self._ctrl.editObject(x, y)
        DiagramFrame.OnLeftDClick(self, event)

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

    def getUmlObjects(self):
        """
        To know all OglObject.

        @since 1.19
        @author L. Burgbacher <lb@alawa.ch>
        """
        # umlObjs = [s for s in self._diagram.GetShapes() if isinstance(s, (OglObject, OglLink, OglSDMessage))]
        umlObjs = []
        for s in self._diagram.GetShapes():
            if isinstance(s, (OglObject, OglLink, OglSDMessage)):
                umlObjs.append(s)
        return umlObjs

    def getWidth(self):
        """
        Knowing Width.

        @since 1.19
        @author Deve Roux <droux@eivd.ch>
        """
        return self.maxWidth

    def getHeight(self):
        """
        Knowing Height.

        @since 1.19
        @author Deve Roux <droux@eivd.ch>
        """
        return self.maxHeight

    def getObjectsBoundaries(self):
        """
        Return object boundaries (coordinates)

        @since 1.35.2.25
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        infinite = 1e9
        minx     = infinite
        maxx     = -infinite
        miny     = infinite
        maxy     = -infinite

        # Get boundaries
        for shapeObject in self._diagram.GetShapes():
            # Get object limits
            ox1, oy1 = shapeObject.GetPosition()
            ox2, oy2 = shapeObject.GetSize()
            ox2 += ox1
            oy2 += oy1

            # Update min-max
            minx = min(minx, ox1)
            maxx = max(maxx, ox2)
            miny = min(miny, oy1)
            maxy = max(maxy, oy2)

        # Return values
        return minx, miny, maxx, maxy

    def getUmlObjectById(self, objectId: int):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (20.11.2005)
        @param objectId    :   id for which we want to get an object

        @return the uml object that has the specified id. If there is no
        matching object, None is returned.
        """

        for shape in self.GetDiagram().GetShapes():
            if isinstance(shape, (OglObject, OglLink)):
                if shape.getPyutObject().getId() == objectId:
                    return shape
        return None

    def getHistory(self):
        """
        Added by P. Dabrowski <przemek.dabrowski@destroy-display.com> (20.11.2005)
        @return the history associated to this frame
        """
        return self._history
