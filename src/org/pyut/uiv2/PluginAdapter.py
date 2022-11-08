
from typing import cast

from logging import Logger
from logging import getLogger

from wx import Yield as wxYield

from core.IPluginAdapter import IPluginAdapter
from core.IPluginAdapter import ScreenMetrics

from core.types.Types import FrameInformationCallback
from core.types.Types import FrameSizeCallback
from core.types.Types import OglObjectType
from core.types.Types import PluginDocument
from core.types.Types import PluginDocumentType
from core.types.Types import PluginProject
from core.types.Types import SelectedOglObjectsCallback

from pyut.enums.DiagramType import DiagramType
from pyut.general.PyutVersion import PyutVersion

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

        ppi: Size        = ScreenDC().GetPPI()
        ds:   DisplaySize = DisplaySize()

        sm: ScreenMetrics = ScreenMetrics()

        sm.screenWidth  = ds[0]
        sm.screenHeight = ds[1]
        sm.dpiX         = ppi[0]
        sm.dpiY         = ppi[1]

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
        self._eventEngine.sendEvent(EventType.FrameSize, callback=callback)

    def getFrameInformation(self, callback: FrameInformationCallback):
        self._eventEngine.sendEvent(EventType.FrameInformation, callback=callback)

    def getSelectedOglObjects(self, callback: SelectedOglObjectsCallback):
        self._eventEngine.sendEvent(EventType.SelectedOglObjects, callback=callback)

    def refreshFrame(self):
        self._eventEngine.sendEvent(EventType.RefreshFrame)

    def selectAllOglObjects(self):
        self._eventEngine.sendEvent(EventType.SelectAllShapes)
        wxYield()

    def deselectAllOglObjects(self):
        self._eventEngine.sendEvent(EventType.DeSelectAllShapes)
        wxYield()

    def addShape(self, shape: OglObjectType):
        """
        Assumes a current frame exists;  This is a check done by the PluginInterfaces
        Args:
            shape:

        Returns:

        """
        self._eventEngine.sendEvent(EventType.AddShape, shapeToAdd=shape)

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
            wxYield()
        # Done project and all diagrams created;  Do not leave any residue around
        self._pluginProject = NO_PLUGIN_PROJECT

    def _diagramCreated(self, pyutDocument: IPyutDocument):

        pluginProject: PluginProject = self._pluginProject

        # find the correct plugin document
        pluginDocument: PluginDocument = cast(PluginDocument, None)
        for document in pluginProject.pluginDocuments.values():
            pluginDocument  = cast(PluginDocument, document)
            if pluginDocument.documentTitle == pyutDocument.title:
                break

        assert pluginDocument is not None, 'Developer error'

        self._layoutPluginDocument(pluginDocument=pluginDocument)

    def _layoutPluginDocument(self, pluginDocument: PluginDocument):
        """
        Loads a plugin's Ogl Objects

        Args:
            pluginDocument: The plugin document itself
        """
        for oglClass in pluginDocument.oglClasses:
            self._layoutAnOglObject(oglObject=oglClass)

        for oglLink in pluginDocument.oglLinks:
            # self._layoutLinks(oglLinks=pluginDocument.oglLinks)
            self._layoutAnOglObject(oglObject=oglLink)

        for oglNote in pluginDocument.oglNotes:
            self._layoutAnOglObject(oglObject=oglNote)

        for oglText in pluginDocument.oglTexts:
            self._layoutAnOglObject(oglObject=oglText)

        for oglUseCase in pluginDocument.oglUseCases:
            self._layoutAnOglObject(oglObject=oglUseCase)

        for oglActor in pluginDocument.oglActors:
            self._layoutAnOglObject(oglObject=oglActor)

        for oglSDInstance in pluginDocument.oglSDInstances.values():
            self._layoutAnOglObject(oglObject=oglSDInstance)

        for oglSDMessage in pluginDocument.oglSDMessages.values():
            self._layoutAnOglObject(oglObject=oglSDMessage)

    def _layoutAnOglObject(self, oglObject: OglObjectType):

        self.addShape(shape=oglObject)      # type ignore

    def _toPyutDiagramType(self, documentType: PluginDocumentType) -> DiagramType:

        if documentType == PluginDocumentType.CLASS_DIAGRAM:
            return DiagramType.CLASS_DIAGRAM
        elif documentType == PluginDocumentType.USECASE_DIAGRAM:
            return DiagramType.USECASE_DIAGRAM
        else:
            return DiagramType.SEQUENCE_DIAGRAM
