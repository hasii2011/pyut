
from typing import cast
from typing import Union

from logging import Logger
from logging import getLogger

from core.IPluginAdapter import IPluginAdapter
from core.IPluginAdapter import ScreenMetrics

from core.types.Types import FrameInformationCallback
from core.types.Types import FrameSizeCallback
from core.types.Types import PluginDocumentType
from core.types.Types import PluginProject
from core.types.Types import SelectedOglObjectsCallback

from ogl.OglLink import OglLink
from ogl.OglObject import OglObject

from org.pyut.enums.DiagramType import DiagramType
from org.pyut.general.PyutVersion import PyutVersion

from org.pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler
from org.pyut.uiv2.IPyutDocument import IPyutDocument
from org.pyut.uiv2.IPyutProject import IPyutProject
from org.pyut.uiv2.eventengine.Events import EventType
from org.pyut.uiv2.eventengine.IEventEngine import IEventEngine
from org.pyut.uiv2.eventengine.eventinformation.NewProjectDiagramInformation import NewProjectDiagramInformation

NO_PLUGIN_PROJECT = cast(PluginProject, None)


class PluginAdapter(IPluginAdapter):

    def __init__(self, eventEngine: IEventEngine):
        """

        Args:
            eventEngine:    The Pyut event engine
        """
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._eventEngine: IEventEngine = eventEngine

        self._pluginProject: PluginProject = NO_PLUGIN_PROJECT  # temp store between callbacks

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
        """

        Args:
            pluginProject:
        """
        self._pluginProject = pluginProject
        filename: str = pluginProject.fileName
        self._eventEngine.sendEvent(EventType.NewNamedProject, projectFilename=filename, callback=self._projectCreated)

    def _projectCreated(self, pyutProject: IPyutProject):

        pluginProject: PluginProject = self._pluginProject

        for pluginDocument in pluginProject.pluginDocuments.values():
            info: NewProjectDiagramInformation = NewProjectDiagramInformation()

            info.pyutProject = pyutProject
            info.diagramType = self._toPyutDiagramType(pluginDocument.documentType)
            info.diagramName = ''
            info.callback    = self._diagramCreated

            self._eventEngine.sendEvent(EventType.NewProjectDiagram, newProjectDiagramInformation=info)

    def _diagramCreated(self, pyutDocument: IPyutDocument):

        self._pluginProject = NO_PLUGIN_PROJECT

        # TODO Layout the diagram

    def _toPyutDiagramType(self, documentType: PluginDocumentType) -> DiagramType:

        if documentType == PluginDocumentType.CLASS_DIAGRAM:
            return DiagramType.CLASS_DIAGRAM
        elif documentType == PluginDocumentType.USECASE_DIAGRAM:
            return DiagramType.USECASE_DIAGRAM
        else:
            return DiagramType.SEQUENCE_DIAGRAM
