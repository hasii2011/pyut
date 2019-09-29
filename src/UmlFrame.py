
from typing import Callable

from logging import Logger
from logging import getLogger

import wx

from PyutClass import PyutClass
from PyutActor import PyutActor
from PyutUseCase import PyutUseCase
from PyutMethod import PyutMethod
from PyutParam import PyutParam
from PyutNote import PyutNote

from OglObject import OglObject
from OglActor import OglActor
from OglUseCase import OglUseCase
from OglClass import OglClass
from OglNote import OglNote
from OglLink import OglLink
from OglSDMessage import OglSDMessage

from MiniOgl import SKIP_EVENT
from MiniOgl import DiagramFrame
from createOglLinkCommand import CreateOglLinkCommand

from mediator import ACTION_ZOOM_IN
from mediator import getMediator

from pyutUtils import displayError

from historyManager import HistoryManager

from globals import _

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
        self.Bind(wx.EVT_CLOSE, self.evtClose)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CHAR, self._ctrl.processChar)

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
        displayError(_("Not yet implemented !"))

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
        wx.BeginBusyCursor()

        from inspect import getfullargspec
        import PyutDataClasses as pdc

        # get a list of classes info for classes in the display list
        # classes = [res[name] for name in res.keys() if name in display]
        # if (type(cl) == ClassType or type(cl) == TypeType or type(cl) == 'module') and cl.__name__ in display]

        self.logger.info(f'pdc value {pdc.__dict__.values()}')
        # classes = [cl for cl in pdc.__dict__.values() if (isinstance(cl, type) or type(cl) == 'module') and cl.__name__ in display]
        classes = []
        for cl in pdc.__dict__.values():
            if (isinstance(cl, type) or type(cl) == 'module') and cl.__name__ in display:
                classes.append(cl)
        objs = {}
        # create the PyutClass objects
        for cl in classes:
            # create objects
            pc = PyutClass(cl.__name__)
            po = OglClass(pc)

            # clmethods = [me for me in cl.__dict__.values() if type(me) == types.FunctionType]
            clmethods = []
            for methd in cl.__dict__.values():
                if isinstance(methd, Callable):
                    self.logger.info(f'method: {methd}')
                    clmethods.append(methd)
            # add the methods
            methods = []
            for me in clmethods:
                funcName: str = me.__name__
                meth = PyutMethod(funcName)
                # add the params
                # if type(me) != types.FunctionType:
                #     try:
                #         me = mobj.__dict__.get("im_func")
                #     except AttributeError:
                #         me = None
                if me is not None:
                    # args = getargspec(me)
                    args = getfullargspec(me)
                    if args[3] is None:
                        firstDefVal = len(args[0])
                    else:
                        firstDefVal = len(args[0]) - len(args[3])
                    for arg, i in zip(args[0], range(len(args[0]))):
                        # don't add self, it's implied
                        defVal = None
                        if arg != "self":
                            if i >= firstDefVal:
                                defVal = args[3][i - firstDefVal]
                                # if type(defVal) == types.StringType:
                                if isinstance(defVal, str):
                                    # defVal = '"' + defVal + '"'
                                    defVal = f'"{defVal}"'
                                param = PyutParam(arg, "", str(defVal))
                            else:
                                param = PyutParam(arg)
                            meth.addParam(param)
                methods.append(meth)
                # set the visibility according to naming conventions
                func_name = funcName
                if func_name[-2:] != "__":
                    if func_name[0:2] == "__":
                        meth.setVisibility("-")
                    elif func_name[0] == "_":
                        meth.setVisibility("#")

            methods = sorted(methods, key=PyutMethod.getName)
            pc.setMethods(methods)
            self.addShape(po, 0, 0)
            po.autoResize()
            objs[cl.__name__] = po

        # now, search for paternity links
        for po in objs.values():
            pc = po.getPyutObject()
            # skip object, it has no parent
            if pc.getName() == "object":
                continue
            currentClass = pdc.__dict__.get(pc.getName())
            fatherClasses = [cl for cl in classes if cl.__name__ in map(lambda z: z.__name__, currentClass.__bases__)]

            def getClassesNames(theList):
                return [item.__name__ for item in theList]

            fatherNames = getClassesNames(fatherClasses)
            for father in fatherNames:
                dest = objs.get(father)
                if dest is not None:  # maybe we don't have the father loaded
                    self.logger.warning(f'Not yet creating inheritance links; po: {po} dest: {dest}')
                    self._createInheritanceLink(po, dest)

        # sort by descending height
        objs = objs.values()
        objs = sorted(objs, key=OglClass.GetHeight)

        # organize by vertical descending sizes
        x = 20
        y = 20
        # incX = 0   NOT USED
        incY = 0
        for po in objs:
            incX, sy = po.GetSize()
            incX += 20
            sy += 20
            incY = max(incY, sy)
            # find good coordinates
            if x + incX >= self.maxWidth:
                x = 20
                y += incY
                incY = sy
            po.SetPosition(x + incX // 2, y + sy // 2)

            x += incX

        wx.EndBusyCursor()

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

    def OnLeftDClick(self, event: wx.MouseEvent):
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

    def _createInheritanceLink(self, child: OglClass, father: OglClass):
        """
        Add a paternity link between child and father.

        Args:
            child:  A child
            father: The daddy!!

        Returns: an OgLink

        """

        cmd: CreateOglLinkCommand = CreateOglLinkCommand(src=father, dst=child)
