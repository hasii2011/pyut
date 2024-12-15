
from typing import Callable
from typing import List
from typing import Dict
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Point

from pyut.ui.umlframes.UmlFrameShapeHandler import UmlFrameShapeHandler

from pyutmodelv2.PyutClass import PyutClass
from pyutmodelv2.PyutMethod import PyutMethods

from pyutmodelv2.enumerations.PyutLinkType import PyutLinkType

from ogl.OglClass import OglClass

from pyut.ui.wxcommands.CommandCreateOglLink import CommandCreateOglLink

from pyut.ui.eventengine.IEventEngine import IEventEngine


class GraphicalHandler:

    def __init__(self, umlFrame: UmlFrameShapeHandler, eventEngine: IEventEngine, maxWidth: int):

        self.logger:          Logger               = getLogger(__name__)
        self._umlFrame:       UmlFrameShapeHandler = umlFrame
        self._maxWidth:       int                  = maxWidth

        self._eventEngine: IEventEngine = eventEngine

    def addHierarchy(self, display):
        """
        Hardcoded example of a class diagram, for test purposes.
        Classes come from self introspection !!!
        OK, it's too big, but it's not a feature, just a toy.

        Args:
            display:
        """
        from pyut.experimental.PythonMetaClassDataHandler import PythonMetaClassDataHandler     # type: ignore

        cg: PythonMetaClassDataHandler = PythonMetaClassDataHandler()
        classes: List[type] = cg.getClassListFromNames(display)

        classNameToOglClass: Dict[str, OglClass] = {}

        # create the Pyut Class objects & associate Ogl graphical classes
        for cl in classes:
            # create objects
            pyutClassDef: PyutClass = PyutClass(cl.__name__)

            klassMethods: List[Callable] = cg.getMethodsFromClass(cl)

            # add the methods
            methods: PyutMethods = cg.generatePyutMethods(cast(PyutMethods, klassMethods))

            # TODO:  Figure out how to use property name as callable -- Kind of works
            # methods = sorted(methods, key=PyutMethod.getName)
            methods.sort(key=lambda pyutMethod: pyutMethod.name, reverse=False)
            pyutClassDef.methods = methods

            oglClassDef = self.addToDiagram(pyutClassDef)
            classNameToOglClass[cl.__name__] = oglClassDef

        oglClassDefinitions: List[OglClass] = list(classNameToOglClass.values())

        self.positionClassHierarchy(oglClassDefinitions)

        # now, search for parent links
        for oglClassDef in classNameToOglClass.values():

            pyutClassDef = cast(PyutClass, oglClassDef.pyutObject)
            # skip object, it has no parent
            if pyutClassDef.name == "object":
                continue

            parentNames = cg.getParentClassNames(classes, pyutClassDef)

            for parent in parentNames:
                dest = classNameToOglClass.get(parent)
                if dest is not None:  # maybe we don't have the parent loaded
                    self.createInheritanceLink(oglClassDef, dest)

    def addToDiagram(self, pyutClassDef: PyutClass) -> OglClass:
        """
        Add graphical version of data class to diagram

        Args:
            pyutClassDef:  The class data

        Returns:  The graphical element created to represent the above in the
        diagram
        """
        oglClassDef: OglClass = OglClass(pyutClassDef)
        self._umlFrame.addShape(oglClassDef, 0, 0)
        oglClassDef.autoResize()
        return oglClassDef

    def createInheritanceLink(self, child: OglClass, parent: OglClass):
        """
        Add a paternity link between child and father.

        Args:
            child:  A child
            parent: The daddy!!

        Returns: an OgLink

        """
        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        childX, childY   = child.GetPosition()
        parentX, parentY = parent.GetPosition()
        sourcePosition:      Point = Point(childX, childY)
        destinationPosition: Point = Point(parentX, parentY)

        command: CommandCreateOglLink = CommandCreateOglLink(eventEngine=self._eventEngine,
                                                             src=child, dst=parent,
                                                             linkType=PyutLinkType.INHERITANCE,
                                                             srcPoint=sourcePosition,
                                                             dstPoint=destinationPosition
                                                             )
        umlDiagramsFrame: UmlDiagramsFrame = cast(UmlDiagramsFrame, self._umlFrame)
        umlDiagramsFrame.commandProcessor.Submit(command=command, storeIt=True)

    def positionClassHierarchy(self, oglClassDefinitions: List[OglClass]):
        """
        Organize by vertical descending sizes

        Args:
            oglClassDefinitions:
        """
        # sort by ascending height
        sortedOglClassDefinitions: List[OglClass] = sorted(oglClassDefinitions, key=OglClass.GetHeight)

        x = 20
        y = 20
        incY = 0
        for oglClassDef in sortedOglClassDefinitions:
            incX, sy = oglClassDef.GetSize()
            incX += 20
            sy += 20
            incY = max(incY, sy)
            # find good coordinates
            if x + incX >= self._maxWidth:
                x = 20
                y += incY
                incY = sy
            oglClassDef.SetPosition(x + incX // 2, y + sy // 2)

            x += incX
