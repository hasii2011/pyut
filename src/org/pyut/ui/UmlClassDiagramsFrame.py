
from typing import cast
from typing import NewType
from typing import Tuple
from typing import Union

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutLink import PyutLink
from org.pyut.enums.LinkType import LinkType
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglLinkFactory import getOglLinkFactory
from org.pyut.ui.UmlDiagramsFrame import UmlDiagramsFrame

UmlClassType       = NewType('UmlClassType', Union[PyutClass, OglClass])
CreatedClassesType = NewType('CreatedClassTypes', Tuple[UmlClassType])


class UmlClassDiagramsFrame(UmlDiagramsFrame):
    """
    UmlClassDiagramsFrame : a UML class diagram frame.

    This class is the instance of one UML class diagram structure.
    It derives its functionalities from UmlDiagramsFrame, but
    as he know the structure of a class diagram,
    he can load class diagram datas.

    Used by FilesHandling.

    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    :version: $Revision: 1.8 $
    """
    def __init__(self, parent):
        """
        Constructor.

        @param wx.Window parent : parent window
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        super().__init__(parent)
        self.newDiagram()

    def createLink(self, src: OglClass, dst: OglClass, linkType: LinkType = LinkType.AGGREGATION):
        """
        Used to create links;  It is still the caller's responsibility to add the created shape to the
        appropriate diagram

        Args:
            src:        The source OglClass
            dst:        The destination OglClass
            linkType:   The type of link
        """
        pyutLink = PyutLink("", linkType=linkType, source=src.getPyutObject(), destination=dst.getPyutObject())

        oglLinkFactory = getOglLinkFactory()
        oglLink = oglLinkFactory.getOglLink(src, pyutLink, dst, linkType)

        src.addLink(oglLink)
        dst.addLink(oglLink)

        src.getPyutObject().addLink(pyutLink)

        return oglLink

    def createInheritanceLink(self, child: OglClass, parent: OglClass) -> OglLink:
        """
        TODO: this is a duplicate of CreateOglLinkCommandCommand._createInheritanceLink (this code adds it to the frame)

        Add a parent link between the child and parent objects.

        Args:
            child:  Child PyutClass
            parent: Parent PyutClass

        Returns:
            The inheritance OglLink
        """
        pyutLink = PyutLink("", linkType=LinkType.INHERITANCE, source=child.getPyutObject(), destination=parent.getPyutObject())
        oglLink = getOglLinkFactory().getOglLink(child, pyutLink, parent, LinkType.INHERITANCE)

        child.addLink(oglLink)
        parent.addLink(oglLink)

        # add it to the PyutClass
        # child.getPyutObject().addParent(parent.getPyutObject())
        childPyutClass:  PyutClass = child.getPyutObject()
        parentPyutClass: PyutClass = parent.getPyutObject()

        childPyutClass.addParent(parentPyutClass)

        self._diagram.AddShape(oglLink)
        self.Refresh()

        return oglLink

    def createInterfaceLink(self, src, dst):
        """
        Adds an OglInterface link between src and dst.

        Args:
            src:    source of the link
            dst:    destination of the link

        Returns: the created OglInterface link
        """
        pyutLink: PyutLink = PyutLink(linkType=LinkType.INTERFACE, source=src, destination=dst)
        oglLink:  OglLink  = OglLink(srcShape=src, pyutLink=pyutLink, dstShape=dst)

        src.addLink(oglLink)
        dst.addLink(oglLink)

        self._diagram.AddShape(oglLink)
        self.Refresh()

        return oglLink

    def createClasses(self, name: str, x: float, y: float) -> CreatedClassesType:
        """
        Create a pair of classes (pyutClass and oglClass)

        Args:
            name: Class Name

            x:  x-coordinate on the uml frame  oglClass
            y:  y coordinate on the uml frame  oglClass

        Returns: A tuple with one of each:  pyutClass and oglClass
        """
        pyutClass: PyutClass = PyutClass()
        pyutClass.setName(name)

        oglClass: OglClass = OglClass(pyutClass, 50, 50)
        # To make this code capable of being debugged
        oglClass.SetPosition(x=x, y=y)
        self.addShape(oglClass, x, y)

        retData: CreatedClassesType = cast(CreatedClassesType, (pyutClass, oglClass))
        return retData
