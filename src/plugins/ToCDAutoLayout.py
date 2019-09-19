
from plugins.PyutToPlugin import PyutToPlugin


class ToCDAutoLayout(PyutToPlugin):
    """
    Auto-layout tool
    @author C.Dutoit <dutoitc@hotmail.com>
    @version $Revision: 1.4 $
    """
    def __init__(self, oglObjects, umlFrame):
        """
        Constructor.

        @param OglObject oglObjects : list of ogl objects
        @param UmlFrame umlFrame : the umlframe of pyut
        """
        PyutToPlugin.__init__(self, oglObjects, umlFrame)

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        """
        return "CD Auto-layout"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        """
        return "C.Dutoit < dutoitc@hotmail.com >"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        """
        return "0.1"

    def getMenuTitle(self):
        """
        Return a menu title string

        @return string
        """
        # Return the menu title as it must be displayed
        return "CD auto-layout"

    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the import will be cancelled.
        """
        return 1

    def doAction(self, umlObjects, selectedObjects, umlFrame):
        """
        Do the tool's action

        @param OglObject [] umlObjects : list of the uml objects of the diagram
        @param OglObject [] selectedObjects : list of the selected objects
        @param UmlFrame umlFrame : the frame of the diagram
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        from OglClass import OglClass
        from time import time

        if umlFrame is None:
            # TODO : display error "No frame selected"
            return

        # Tractions
        for i in range(20):     # len(umlObjects)):
            for obj in selectedObjects:
                if isinstance(obj, OglClass):
                    self._step(obj)

            # Animation
            # umlFrame.Refresh() # TODO hasii figure out what the replacement is
            t = time()
            while time() < t + 0.005:
                pass

    def _step(self, srcShape):
        from math import sqrt
        ForceField = 200
        vx = 0
        vy = 0
        srcX, srcY = srcShape.GetPosition()
        # print "src = ", srcX, srcY
        for link in srcShape.getLinks():
            dstShape = link.getDestinationShape()
            if dstShape != srcShape:
                dstX, dstY = dstShape.GetPosition()
                linkSize = sqrt((dstX-srcX) * (dstX-srcX) + (dstY-srcY) * (dstY-srcY))
                # print "dst = ", dstX, dstY
                # print "LinkSize = ", linkSize
                n = linkSize-ForceField
                attraction = max(-ForceField/8, min(ForceField/8, n*n*n))
                # print "attraction = ", attraction
                vx += attraction*(dstX-srcX)/linkSize
                vy += attraction*(dstY-srcY)/linkSize
        # print "vx, vy = ", vx, vy
        srcShape.SetPosition(srcX + vx, srcY + vy)
