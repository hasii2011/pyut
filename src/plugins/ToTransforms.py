

from plugins.PyutToPlugin import PyutToPlugin


class ToTransforms(PyutToPlugin):
    """
    A plugin for making transformations : translation, rotations, ...

    @author C.Dutoit <dutoitc@hotmail.com>
    @version $Revision: 1.4 $
    """
    def __init__(self, oglObjects, umlFrame):
        """
        Constructor.

        @param OglObject oglObjects : list of ogl objects
        @param UmlFrame umlFrame : the umlframe of pyut
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        PyutToPlugin.__init__(self, oglObjects, umlFrame)
        self._oglObjects = oglObjects
        self._umlFrame = umlFrame


    #>------------------------------------------------------------------------

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return "Transformations"


    #>------------------------------------------------------------------------

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return "C.Dutoit"


    #>------------------------------------------------------------------------

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return "1.0"


    #>------------------------------------------------------------------------

    def getMenuTitle(self):
        """
        Return a menu title string

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        # Return the menu title as it must be displayed
        return "Transformations"

    #>------------------------------------------------------------------------


    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the import will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return 1


    #>------------------------------------------------------------------------

    def doAction(self, umlObjects, selectedObjects, umlFrame):
        """
        Do move classes

        @param OglObject [] umlObjects : list of the uml objects of the diagram
        @param OglObject [] selectedObjects : list of the selected objects
        @param UmlFrame umlFrame : the frame of the diagram
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if umlFrame is None:
            # TODO : displayError "No frame opened"
            return

        (frameW, frameH) = self._umlFrame.GetSizeTuple()
        for obj in umlObjects:
            x, y = obj.GetPosition()
            obj.SetPosition(frameW-x, y)
