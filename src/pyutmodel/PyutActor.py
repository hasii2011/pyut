
from pyutmodel.PyutLinkedObject import PyutLinkedObject


class PyutActor(PyutLinkedObject):
    """
    Represents a Use Case actor (data layer).
    An actor, in data layer, only has a name. Linking is resolved by
    parent class `PyutLinkedObject` that defines everything needed for
    links connections.


    """
    def __init__(self, actorName: str = ''):
        """
        Args:
            actorName: The name of the actor
        """
        super().__init__(actorName)
