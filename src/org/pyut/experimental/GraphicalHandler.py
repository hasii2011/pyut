
from typing import List
from typing import Dict

from logging import Logger
from logging import getLogger

from org.pyut.ui.UmlFrameShapeHandler import UmlFrameShapeHandler

from org.pyut.commands.CommandGroup import CommandGroup
from org.pyut.commands.CreateOglLinkCommand import CreateOglLinkCommand

from org.pyut.history.HistoryManager import HistoryManager

from org.pyut.PyutClass import PyutClass
from org.pyut.PyutMethod import PyutMethod

from org.pyut.ogl.OglClass import OglClass


class GraphicalHandler:

    def __init__(self, umlFrame: UmlFrameShapeHandler, maxWidth: int, historyManager: HistoryManager):

        self.logger:    Logger   = getLogger(__name__)
        self._umlFrame: UmlFrameShapeHandler = umlFrame
        self._maxWidth: int      = maxWidth
        self._historyManager: HistoryManager = historyManager

    def addHierarchy(self, display):
        """
        Hardcoded example of a class diagram, for test purposes.
        Classes come from self introspection !!!
        OK, it's too big, but it's not a feature, just a toy.

        @author L. Burgbacher <lb@alawa.ch>
        @since 1.4
        """
        # BeginBusyCursor()

        from org.pyut.experimental.PythonMetaClassDataHandler import PythonMetaClassDataHandler

        cg: PythonMetaClassDataHandler = PythonMetaClassDataHandler()
        classes: List[type] = cg.getClassListFromNames(display)

        classNameToOglClass: Dict[str, OglClass] = {}

        graphicalHandler: GraphicalHandler = GraphicalHandler(umlFrame=self._umlFrame, maxWidth=self._maxWidth, historyManager=self._historyManager)
        # create the Pyut Class objects & associate Ogl graphical classes
        for cl in classes:
            # create objects
            pyutClassDef: PyutClass = PyutClass(cl.__name__)

            clmethods: List[classmethod] = cg.getMethodsFromClass(cl)

            # add the methods
            methods: List[PyutMethod] = cg.generatePyutMethods(clmethods)
            methods = sorted(methods, key=PyutMethod.getName)

            pyutClassDef.setMethods(methods)

            oglClassDef = graphicalHandler.addToDiagram(pyutClassDef)
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
                    graphicalHandler.createInheritanceLink(oglClassDef, dest)

        oglClassDefinitions: List[OglClass] = list(classNameToOglClass.values())

        graphicalHandler.positionClassHierarchy(oglClassDefinitions)

        # EndBusyCursor()

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

    def createInheritanceLink(self, child: OglClass, father: OglClass):
        """
        Add a paternity link between child and father.

        Args:
            child:  A child
            father: The daddy!!

        Returns: an OgLink

        """
        cmdGroup: CommandGroup         = CommandGroup('Creating an inheritance link')
        cmd:      CreateOglLinkCommand = CreateOglLinkCommand(src=father, dst=child)

        cmdGroup.addCommand(cmd)
        self._historyManager.addCommandGroup(cmdGroup)

        cmd.execute()

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
