
from typing import cast

from logging import Logger
from logging import getLogger

from copy import deepcopy

from wx import Command
from wx import CommandProcessor
from wx import Point

from wx import Yield as wxYield

from miniogl.ControlPoint import ControlPoint
from miniogl.LineShape import ControlPoints

from ogl.OglLink import OglLink
from ogl.OglPosition import OglPosition
from ogl.OglPosition import OglPositions

from pyutplugins.ExternalTypes import CurrentProjectCallback
from pyutplugins.ExternalTypes import FrameInformationCallback
from pyutplugins.ExternalTypes import FrameSizeCallback
from pyutplugins.ExternalTypes import OglObjectType
from pyutplugins.ExternalTypes import PluginDocument
from pyutplugins.ExternalTypes import PluginDocumentType
from pyutplugins.ExternalTypes import PluginProject
from pyutplugins.ExternalTypes import SelectedOglObjectsCallback
from pyutplugins.ExternalTypes import CreatedLinkCallback
from pyutplugins.ExternalTypes import LinkInformation
from pyutplugins.ExternalTypes import ObjectBoundaries
from pyutplugins.ExternalTypes import ObjectBoundaryCallback
from pyutplugins.ExternalTypes import IntegerList
from pyutplugins.ExternalTypes import Points
from pyutplugins.ExternalTypes import Rectangle
from pyutplugins.ExternalTypes import Rectangles

from pyutplugins.IPluginAdapter import IPluginAdapter
from pyutplugins.IPluginAdapter import ScreenMetrics

from pyut import __version__ as pyutVersion

from pyut.enums.DiagramType import DiagramType

from pyut.ui.CurrentDirectoryHandler import CurrentDirectoryHandler

from pyut.ui.umlframes.UmlDiagramsFrame import UmlDiagramsFrame

from pyut.ui.wxcommands.CommandCreateOglLink import CommandCreateOglLink
from pyut.ui.wxcommands.CommandDeleteOglLink import CommandDeleteOglLink

from pyut.ui.IPyutDocument import IPyutDocument
from pyut.ui.IPyutProject import IPyutProject

from pyut.ui.eventengine.EventType import EventType
from pyut.ui.eventengine.IEventEngine import IEventEngine
from pyut.ui.eventengine.eventinformation.NewProjectDiagramInformation import NewProjectDiagramInformation

NO_PLUGIN_PROJECT           = cast(PluginProject, None)
NO_OBJECT_BOUNDARY_CALLBACK = cast(ObjectBoundaryCallback, None)
NO_OGL_LINK                 = cast(OglLink, None)
NO_LINK_INFORMATION         = cast(LinkInformation, None)


class PluginAdapter(IPluginAdapter):

    def __init__(self, eventEngine: IEventEngine):
        """

        Args:
            eventEngine:    The Pyut event engine
        """
        super().__init__()
        self.logger: Logger = getLogger(__name__)

        self._eventEngine: IEventEngine = eventEngine

        self._pluginProject:   PluginProject          = NO_PLUGIN_PROJECT             # temp save between callbacks
        self._saveCallback:    ObjectBoundaryCallback = NO_OBJECT_BOUNDARY_CALLBACK   # temp save
        self._oglLink:         OglLink                = NO_OGL_LINK                   # temp save
        self._linkInformation: LinkInformation        = NO_LINK_INFORMATION           # temp save

    @property
    def pyutVersion(self) -> str:
        return pyutVersion

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

    def requestCurrentProject(self, callback: CurrentProjectCallback):
        self._eventEngine.sendEvent(EventType.RequestCurrentProject, callback=callback)

    def indicatePluginModifiedProject(self):
        self._eventEngine.sendEvent(EventType.UMLDiagramModified)

    def loadProject(self, pluginProject: PluginProject):
        """

        Args:
            pluginProject:
        """
        self._pluginProject = pluginProject
        filename: str = pluginProject.fileName
        self._eventEngine.sendEvent(EventType.NewNamedProject, projectFilename=filename, callback=self._projectCreated)

    def getObjectBoundaries(self, callback: ObjectBoundaryCallback):
        self._saveCallback = callback
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._onObjectBoundariesActiveUmlFrame)

    def deleteLink(self, oglLink: OglLink):

        self._oglLink = oglLink
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._onDeleteLinkActiveUmlFrame)

    def createLink(self, linkInformation: LinkInformation, callback: CreatedLinkCallback):

        self._linkInformation = linkInformation
        self._eventEngine.sendEvent(EventType.ActiveUmlFrame, callback=self._onCreateLinkActiveUmlFrame)
        wxYield()   # make sure we process the above event first

    def showOrthogonalRoutingPoints(self, show: bool, spots: Points):
        """
        This is currently only a debug entry point.  I am not
        sure if I should keep this.  I am going to go fast and break
        things and correct them later.  Go DOGE

        Args:
            show:   Show or not
            spots:  What the Orthogonal Line router calls these (only valid whe
            `show` is True
        """
        self._eventEngine.sendEvent(EventType.ShowOrthogonalRoutingPoints, show=show, points=spots)

    def showRulers(self, show: bool, horizontalRulers: IntegerList, verticalRulers: IntegerList, diagramBounds: Rectangle):
        self._eventEngine.sendEvent(EventType.ShowRulers,
                                    show=show,
                                    horizontalRulers=horizontalRulers,
                                    verticalRulers=verticalRulers,
                                    diagramBounds=diagramBounds
                                    )

    def showRouteGrid(self, show: bool, routeGrid: Rectangles):
        self._eventEngine.sendEvent(EventType.ShowRouteGrid, show=show, routeGrid=routeGrid)

    def _onObjectBoundariesActiveUmlFrame(self, activeFrame: UmlDiagramsFrame):

        objectBoundaries: ObjectBoundaries = activeFrame.objectBoundaries

        assert self._saveCallback != NO_OBJECT_BOUNDARY_CALLBACK, 'Developer forgot to save the eventHandler'

        self._saveCallback(objectBoundaries)

        self._saveCallback = NO_OBJECT_BOUNDARY_CALLBACK

    def _onDeleteLinkActiveUmlFrame(self, activeFrame: UmlDiagramsFrame):

        assert self._oglLink != NO_OGL_LINK, 'Developer forgot to save the link to delete'
        commandProcessor: CommandProcessor = activeFrame.commandProcessor
        cmd:              Command          = CommandDeleteOglLink(oglLink=self._oglLink, eventEngine=self._eventEngine)
        submitStatus:      bool            = commandProcessor.Submit(command=cmd, storeIt=True)
        self.logger.debug(f'{submitStatus=}')

        self._oglLink = NO_OGL_LINK
        self.refreshFrame()

    def _onCreateLinkActiveUmlFrame(self, activeFrame: UmlDiagramsFrame):

        assert self._linkInformation != NO_LINK_INFORMATION

        commandProcessor: CommandProcessor = activeFrame.commandProcessor

        sourcePoint:      OglPosition = self._linkInformation.path[0]
        destinationPoint: OglPosition = self._linkInformation.path[-1]
        command: CommandCreateOglLink = CommandCreateOglLink(eventEngine=self._eventEngine,
                                                             src=self._linkInformation.sourceShape,
                                                             dst=self._linkInformation.destinationShape,
                                                             linkType=self._linkInformation.linkType,
                                                             srcPoint=self._toWxPoint(sourcePoint),
                                                             dstPoint=self._toWxPoint(destinationPoint),
                                                             )
        command.controlPoints = self._toControlPoints(self._linkInformation.path)
        submitStatus: bool            = commandProcessor.Submit(command=command, storeIt=True)
        self.logger.warning(f'{submitStatus=}')

        self.refreshFrame()

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
        self._eventEngine.sendEvent(EventType.RefreshFrame)

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

    def _toWxPoint(self, oglPosition: OglPosition) -> Point:

        return Point(x=oglPosition.x, y=oglPosition.y)

    def _toControlPoints(self, path: OglPositions) -> ControlPoints:

        pathCopy: OglPositions = deepcopy(path)
        pathCopy.pop(0)     # remove start
        pathCopy = OglPositions(pathCopy[:-1])

        controlPoints: ControlPoints = ControlPoints([])
        for pt in pathCopy:
            point: OglPosition = cast(OglPosition, pt)
            controlPoint: ControlPoint = ControlPoint(x=point.x, y=point.y)
            controlPoint.visible   = True
            controlPoint.draggable = True

            controlPoints.append(controlPoint)

        return controlPoints
