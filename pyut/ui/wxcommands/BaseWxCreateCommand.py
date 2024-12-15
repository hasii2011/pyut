
from typing import TYPE_CHECKING

from logging import Logger
from logging import getLogger

from abc import ABCMeta
from abc import abstractmethod

from pyut.preferences.PyutPreferences import PyutPreferences

from pyut.ui.wxcommands.BaseWxCommand import BaseWxCommand
from pyut.ui.wxcommands.Types import DoableObjectType

from pyut.ui.eventengine.Events import EventType
from pyut.ui.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

# Defines the classes that we can do and undo


class MyMetaBaseWxCommand(ABCMeta, type(BaseWxCommand)):        # type: ignore
    """
    I have no idea why this works:
    https://stackoverflow.com/questions/66591752/metaclass-conflict-when-trying-to-create-a-python-abstract-class-that-also-subcl
    """
    pass


class BaseWxCreateCommand(BaseWxCommand, metaclass=MyMetaBaseWxCommand):
    """
    Base command for commands that create UML objects and associate and edit dialog with them.
    This class implements the .GetName method for all subclasses
    This class implements the basic command methods.
    """
    clsLogger: Logger = getLogger(__name__)

    def __init__(self, canUndo: bool, name: str, eventEngine: IEventEngine, x: int, y: int):

        super().__init__(canUndo=canUndo, name=name)

        self._oglObjX:     int = x
        self._oglObjY:     int = y
        self._eventEngine: IEventEngine = eventEngine
        self._name:        str = name

        self._prefs: PyutPreferences  = PyutPreferences()
        self._shape: DoableObjectType = self._createPrototypeInstance()
        #
        # Save these for later
        #
        w, h = self._shape.GetSize()
        self._oglObjWidth:  int = w
        self._oglObjHeight: int = h

    def GetName(self) -> str:
        return self._name

    def CanUndo(self):
        return True

    def Do(self) -> bool:
        self._placeShapeOnFrame()
        return True

    def Undo(self) -> bool:
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._cbGetActiveUmlFrameForUndo)
        return True

    @abstractmethod
    def _createPrototypeInstance(self) -> DoableObjectType:
        """
        Creates an appropriate class for the new command

        Returns:    The newly created class
        """
        pass

    @abstractmethod
    def _placeShapeOnFrame(self):
        """
        Implemented by subclasses to support .Do
        """
        pass

    def _cbGetActiveUmlFrameForUndo(self, frame: 'UmlDiagramsFrame'):
        """
        This is the default simple behavior;  If you need more complex
         behavior, override this method

        Args:
            frame:
        """
        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame

        self._shape.Detach()
        umlFrame.Refresh()

    def _cbAddOglObjectToFrame(self, frame: 'UmlDiagramsFrame'):
        """
        This is common code needed to create Note, Text, Actor, and UseCase shapes.

        Args:
            frame:
        """

        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame
        self.clsLogger.info(f'{umlFrame=}')

        umlFrame.addShape(self._shape, self._oglObjX, self._oglObjY, withModelUpdate=True)

        umlFrame.Refresh()
