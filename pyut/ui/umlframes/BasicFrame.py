from typing import Protocol

from wx import CommandProcessor

from ogl.events.OglEventEngine import OglEventEngine


class BasicFrame(Protocol):
    """
    Stand in object for UmlFrame which has the command processor
    Stand in object for UmlDiagramsFrame which has the event engine
    """

    commandProcessor: CommandProcessor
    eventEngine:      OglEventEngine
