

from UmlFrame import *

from UmlDiagramsFrame import *
from PyutSDInstance import *
from PyutSDMessage import *
from OglSDInstance import *

from PyutConsts import OGL_SD_MESSAGE


class UmlSequenceDiagramsFrame(UmlDiagramsFrame):
    """
    UmlSequenceDiagramsFrame : a UML sequence diagram frame.

    This class is the instance of one UML sequence diagram structure.
    It derives its functionalities from UmlDiagramsFrame, but
    as he know the structure of a sequence diagram,
    he can load sequence diagram datas.

    Used by FilesHandling.

    :Note on datas:
        - cdInstances is a set of class diagram instances,
          composed by label and lifeline


    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    :version: $Revision: 1.11 $
    """

    #>------------------------------------------------------------------------

    def __init__(self, parent):
        """
        Constructor.

        @param wx.Window parent : parent window
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        import os
        UmlDiagramsFrame.__init__(self, parent)
        self.newDiagram()
        self._cdInstances = []

    #>-----------------------------------------------------------------------

    def createNewSDInstance(self, x, y):
        """
        Create a new class diagram instance

        @author C.Dutoit
        """
        # Create and add instance
        pyutSDInstance = PyutSDInstance()
        oglSDInstance  = OglSDInstance(pyutSDInstance, self)
        self.addShape(oglSDInstance, x, oglSDInstance.GetPosition()[1])
        return pyutSDInstance

    #>-----------------------------------------------------------------------

    #def OnOpen(self, filename):
        #"""
        #Open datas from a file
#
        #@return True if the file has been loaded, False in others cases
        #@since 1.0
        #@author C.Dutoit <dutoitc@hotmail.com>
        #"""
        ##Init loading
        #self.newDiagram()
#
        ##Return with success
        #wx.EndBusyCursor()
        #return True

    #>-----------------------------------------------------------------------

    #def onClose(self, force=False):
        #"""
        #Closing handler (must be called explicitly).
        #Save files and ask for confirmation.
#
        #@return True if the close succeeded
        #@since 1.0
        #@author C.Dutoit <dutoitc@hotmail.com>
        #"""
        #self.cleanUp()
        ##wx.OGLCleanUp()
        #self.Destroy(-1)
        #return True


    #>------------------------------------------------------------------------

    def createNewLink(self, src, dst, type=OGL_SD_MESSAGE,
                      srcPos = None, dstPos = None):
        """
        Add a link between src and dst.

        @param OglSDInstance src  : source of the link
        @param OglSDInstance dst  : destination of the link
        @param int type : type of the link
        @param srcPos, dstPos : position on source and destination
        @return OglLink : the link created
        @author L. Burgbacher
        @modified C.Dutoit 20021125 : added srcPos and dstPos to be compatible
                                with Sequence diagram
        """
        #pyutLink = PyutLink("", type=type,
        #    source=src.getPyutObject(),
        #    destination=dst.getPyutObject())
        srcTime = src.ConvertCoordToRelative(0, srcPos[1])[1]
        dstTime = dst.ConvertCoordToRelative(0, dstPos[1])[1]
        #srcTime=srcPos[1] - src.GetPosition()[1]
        #dstTime=dstPos[1] - dst.GetPosition()[1]
        #print "CreateNewLink - ", srcTime, dstTime
        #print ", src/dst=", src, dst
        pyutLink = PyutSDMessage("msg test", src.getPyutObject(), srcTime,
                                             dst.getPyutObject(), dstTime)

        # Call the factory to create OGL Link
        oglLink = OglSDMessage(src, pyutLink, dst)
        pyutLink.setOglObject(oglLink)
        #print "createNewLink2 - ", oglLink.GetSegments()


        src.addLink(oglLink)  # add it to the source OglShape
        dst.addLink(oglLink)  # add it to the destination OglShape
        self._diagram.AddShape(oglLink) # add it to the diagram
        #self._diagram.Refresh()
        self.Refresh()


        return oglLink
