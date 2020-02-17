
from org.pyut.model.PyutLinkedObject import PyutLinkedObject


class PyutActor(PyutLinkedObject):
    """
    Represents a Use Case actor (data layer).
    An actor, in data layer, only has a name. Linking is resolved by
    parent class `PyutLinkedObject` that defines everything needed for
    links connections.

    :version: $Revision: 1.3 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """
    def __init__(self, actorName: str = ""):
        """
        Constructor.
        @param actorName : The name of the actor

        @since 1.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        super().__init__(actorName)
