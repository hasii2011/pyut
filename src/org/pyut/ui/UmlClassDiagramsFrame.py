
from typing import cast

from collections import namedtuple

from org.pyut.history.commands.CommandGroup import CommandGroup
from org.pyut.history.commands.CreateOglClassCommand import CreateOglClassCommand
from org.pyut.history.commands.CreateOglLinkCommand import CreateOglLinkCommand

from pyutmodel.ModelTypes import ClassName
from pyutmodel.ModelTypes import Implementors
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutInterface import PyutInterface
from pyutmodel.PyutLink import PyutLink

from pyutmodel.PyutLinkType import PyutLinkType

from ogl.OglClass import OglClass
from ogl.OglInterface import OglInterface
from ogl.OglInterface2 import OglInterface2
from ogl.OglLinkFactory import getOglLinkFactory

from org.pyut.ui.UmlDiagramsFrame import UmlDiagramsFrame
from org.pyut.ui.umlframes.UmlFrame import UmlObjects

from org.pyut.general.CustomEvents import ClassNameChangedEvent
from org.pyut.general.CustomEvents import EVT_CLASS_NAME_CHANGED


CreatedClassesType = namedtuple('CreatedClassesType', 'pyutClass, oglClass')


class UmlClassDiagramsFrame(UmlDiagramsFrame):

    cdfDebugId: int = 0x000FF   # UML Class Diagrams Frame Debug ID

    """
    UmlClassDiagramsFrame : a UML class diagram frame.

    This class is the instance of one UML class diagram structure.
    It derives its functionality from UmlDiagramsFrame, but
    it knows the structure of a class diagram and it can load class diagram data.
    """
    def __init__(self, parent):
        """
        """

        self._cdfDebugId: int = UmlClassDiagramsFrame.cdfDebugId

        UmlClassDiagramsFrame.cdfDebugId += 1

        super().__init__(parent)
        self.newDiagram()

        self.Bind(EVT_CLASS_NAME_CHANGED, self._onClassNameChanged)

    def createClass(self, oglClass: OglClass):

        x, y = oglClass.GetPosition()

        cmdGroup: CommandGroup         = CommandGroup("Create class")
        cmd:     CreateOglClassCommand = CreateOglClassCommand(x=x, y=y, oglClass=oglClass)
        cmdGroup.addCommand(cmd)
        self.getHistory().addCommandGroup(cmdGroup)
        cmd.execute()

    def createLink(self, src: OglClass, dst: OglClass, linkType: PyutLinkType = PyutLinkType.AGGREGATION):
        """
        Used to create links;  It is still the caller's responsibility to add the created shape to the
        appropriate diagram

        Args:
            src:        The source OglClass
            dst:        The destination OglClass
            linkType:   The type of link
        """
        sourceClass:      PyutClass = cast(PyutClass, src.pyutObject)
        destinationClass: PyutClass = cast(PyutClass, dst.pyutObject)

        pyutLink: PyutLink = PyutLink("", linkType=linkType, source=sourceClass, destination=destinationClass)

        oglLinkFactory = getOglLinkFactory()
        oglLink = oglLinkFactory.getOglLink(src, pyutLink, dst, linkType)

        src.addLink(oglLink)
        dst.addLink(oglLink)

        pyutClass: PyutClass = cast(PyutClass, src.pyutObject)
        pyutClass.addLink(pyutLink)

        return oglLink

    def createInheritanceLink(self, child: OglClass, parent: OglClass):
        """
        Add a parent link between the child and parent objects.

        Args:
            child:  Child PyutClass
            parent: Parent PyutClass

        """
        cmdGroup: CommandGroup         = CommandGroup('Creating an inheritance link')
        cmd:      CreateOglLinkCommand = CreateOglLinkCommand(src=child, dst=parent)    # inheritance points back to parent
        cmdGroup.addCommand(cmd)
        self._historyManager.addCommandGroup(cmdGroup)

        cmd.execute()

    def createInterfaceLink(self, src: OglClass, dst: OglClass) -> OglInterface:
        """
        Adds an OglInterface link between src and dst.

        Args:
            src:    source of the link
            dst:    destination of the link

        Returns: the created OglInterface link
        """
        sourceClass:      PyutClass = cast(PyutClass, src.pyutObject)
        destinationClass: PyutClass = cast(PyutClass, dst.pyutObject)

        pyutLink:     PyutLink     = PyutLink(linkType=PyutLinkType.INTERFACE, source=sourceClass, destination=destinationClass)
        oglInterface: OglInterface = OglInterface(srcShape=src, pyutLink=pyutLink, dstShape=dst)

        src.addLink(oglInterface)
        dst.addLink(oglInterface)

        self._diagram.AddShape(oglInterface)
        self.Refresh()

        return oglInterface

    def createClasses(self, name: str, x: int, y: int) -> CreatedClassesType:
        """
        Create a pair of classes (pyutClass and oglClass)

        Args:
            name: Class Name

            x:  x-coordinate on the uml frame  oglClass
            y:  y coordinate on the uml frame  oglClass

        Returns: A named tuple with attributes:  pyutClass and oglClass
        """
        pyutClass: PyutClass = PyutClass()
        pyutClass.name = name

        oglClass: OglClass = OglClass(pyutClass, 50, 50)
        # To make this code capable of being debugged
        oglClass.SetPosition(x=x, y=y)
        self.addShape(oglClass, x, y)

        createdClasses: CreatedClassesType = CreatedClassesType(pyutClass=pyutClass, oglClass=oglClass)

        return createdClasses

    def _onClassNameChanged(self, event: ClassNameChangedEvent):

        oldClassName: ClassName = ClassName(event.oldClassName)
        newClassName: ClassName = ClassName(event.newClassName)
        self.logger.warning(f'{oldClassName=} {newClassName=}')

        umlObjects: UmlObjects = self.getUmlObjects()

        for umlObject in umlObjects:
            if isinstance(umlObject, OglInterface2):
                oglInterface:  OglInterface2 = cast(OglInterface2, umlObject)
                pyutInterface: PyutInterface = oglInterface.pyutInterface

                implementors: Implementors = pyutInterface.implementors

                for idx, implementor in enumerate(implementors):
                    self.logger.warning(f'{idx=} - {pyutInterface.name=} {implementor=}')
                    if implementor == oldClassName:
                        pyutInterface.implementors[idx] = newClassName

    def __repr__(self) -> str:

        debugId: str = f'0x{self._cdfDebugId:06X}'
        return f'UmlClassDiagramsFrame:[{debugId=}]'
