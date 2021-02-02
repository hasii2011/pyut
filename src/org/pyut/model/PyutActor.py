
from org.pyut.model.PyutLinkedObject import PyutLinkedObject
from org.pyut.preferences.PyutPreferences import PyutPreferences


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

        if actorName is None or actorName == '':
            actorName = PyutPreferences().actorName

        super().__init__(actorName)
