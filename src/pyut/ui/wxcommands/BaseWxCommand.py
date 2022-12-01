
from typing import TYPE_CHECKING
from typing import Union

from abc import ABCMeta
from abc import abstractmethod

from wx import Command

from ogl.OglLink import OglLink
from ogl.OglObject import OglObject
from ogl.OglInterface2 import OglInterface2

from pyut.preferences.PyutPreferences import PyutPreferences
from pyut.uiv2.eventengine.Events import EventType

from pyut.uiv2.eventengine.IEventEngine import IEventEngine

if TYPE_CHECKING:
    from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

# Defines the classes that we can do and undo
DoableClass  = Union[OglObject, OglLink, OglInterface2]


class MyMeta(ABCMeta, type(Command)):        # type: ignore
    """
    I have know idea why this works:
    https://stackoverflow.com/questions/66591752/metaclass-conflict-when-trying-to-create-a-python-abstract-class-that-also-subcl
    """
    pass


class BaseWxCommand(Command, metaclass=MyMeta):
    """
    Base command for commands that create UML objects and associate and edit dialog with them.
    This class implements the .GetName method for all subclasses
    This class implements the .
    """
    def __init__(self, canUndo: bool, name: str, eventEngine: IEventEngine, x: int, y: int, oglObject: DoableClass | None = None):

        super().__init__(canUndo=canUndo, name=name)

        self._oglObjX:     int = x
        self._oglObjY:     int = y
        self._eventEngine: IEventEngine = eventEngine
        self._name:        str = name

        self._prefs: PyutPreferences = PyutPreferences()

        if oglObject is None:
            self._shape:            DoableClass = self._createNewObject()
            self._invokeEditDialog: bool     = True
        else:
            self._shape            = oglObject
            self._invokeEditDialog = False
        #
        # Get either the new width & height or the one from the incoming object
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
    def _createNewObject(self) -> DoableClass:
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
        behavior override this method

        Args:
            frame:
        """
        from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

        umlFrame: UmlDiagramsFrame = frame

        self._shape.Detach()
        umlFrame.Refresh()
