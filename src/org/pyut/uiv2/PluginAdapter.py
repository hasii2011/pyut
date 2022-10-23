
from typing import Union

from logging import Logger
from logging import getLogger

from core.IPluginAdapter import IPluginAdapter
from core.IPluginAdapter import ScreenMetrics

from core.types.Types import FrameInformationCallback
from core.types.Types import FrameSizeCallback
from core.types.Types import PluginProject
from core.types.Types import SelectedOglObjectsCallback

from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from org.pyut.general.PyutVersion import PyutVersion

from org.pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler
from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine


class PluginAdapter(IPluginAdapter):

    def __init__(self, eventEngine: IEventEngine):
        """

        Args:
            eventEngine:    The Pyut event engine
        """
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._eventEngine: IEventEngine = eventEngine

    @property
    def pyutVersion(self) -> str:
        return PyutVersion.getPyUtVersion()

    @pyutVersion.setter
    def pyutVersion(self, newVersion: str):
        """
        Does nothing
        Args:
            newVersion:
        """
        pass

    @property
    def screenMetrics(self) -> ScreenMetrics:
        from wx import ScreenDC
        from wx import DisplaySize
        from wx import Size

        size: Size        = ScreenDC().GetPPI()
        ds:   DisplaySize = DisplaySize()

        sm: ScreenMetrics = ScreenMetrics()

        sm.screenWidth = size.GetWidth()
        sm.screenHeight = size.GetHeight()
        sm.dpiX         = ds.GetWidth()
        sm.dpiY         = ds.GetHeight()

        return sm

    @property
    def currentDirectory(self) -> str:
        return CurrentDirectoryHandler().currentDirectory

    @currentDirectory.setter
    def currentDirectory(self, newValue: str):
        """
        Does nothing
        Args:
            newValue:
        """
        pass

    def getFrameSize(self, callback: FrameSizeCallback):
        pass

    def getFrameInformation(self, callback: FrameInformationCallback):
        pass

    def getSelectedOglObjects(self, callback: SelectedOglObjectsCallback):
        pass

    def refreshFrame(self):
        pass

    def selectAllOglObjects(self):
        pass

    def deselectAllOglObjects(self):
        pass

    def addShape(self, shape: Union[OglObject, OglLink]):
        pass

    def loadProject(self, pluginProject: PluginProject):
        pass
