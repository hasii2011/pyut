
from org.pyut.model.PyutLinkedObject import PyutLinkedObject


class PyutActor(PyutLinkedObject):

    DEFAULT_ACTOR_NAME: str = 'Actor'

    """
    Represents a Use Case actor (data layer).
    An actor, in data layer, only has a name. Linking is resolved by
    parent class `PyutLinkedObject` that defines everything needed for
    links connections.


    """
    def __init__(self, actorName: str = DEFAULT_ACTOR_NAME):
        """
        Args:
            actorName: The name of the actor
        """
        super().__init__(actorName)
