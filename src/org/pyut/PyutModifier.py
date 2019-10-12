

class PyutModifier:
    """
    Modifier for a method or param.
    These are words like "abstract", "virtual", "const"...

    :author: Laurent Burgbacher
    :contact: <lb@alawa.ch>
    :version: $Revision: 1.4 $
    """
    def __init__(self, modifierTypeName: str = ""):
        """
        Constructor.

        @param  for the type
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        self.__name = modifierTypeName

    def getName(self):
        """
        Get method, used to know the name.

        @return string name
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self.__name

    def __str__(self):
        """
        String representation.

        @return type : string
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        return self.getName()
