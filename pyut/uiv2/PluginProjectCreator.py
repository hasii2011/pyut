from typing import cast

from logging import Logger
from logging import getLogger

from ogl.OglInterface2 import OglInterface2
from ogl.OglClass import OglClass
from ogl.OglLink import OglLink
from ogl.OglNote import OglNote
from ogl.OglText import OglText
from ogl.OglActor import OglActor
from ogl.OglUseCase import OglUseCase
from ogl.sd.OglSDInstance import OglSDInstance
from ogl.sd.OglSDMessage import OglSDMessage
from oglio import OglVersion

from pyutplugins.ExternalTypes import PluginDocument
from pyutplugins.ExternalTypes import PluginDocumentTitle
from pyutplugins.ExternalTypes import PluginDocumentType
from pyutplugins.ExternalTypes import PluginProject

from pyut.uiv2.IPyutDocument import IPyutDocument
from pyut.uiv2.IPyutProject import IPyutProject
from pyut.uiv2.Types import UmlFrameType


class PluginProjectCreator:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def toPluginProject(self, pyutProject: IPyutProject) -> PluginProject:
        pass

        pluginProject: PluginProject = PluginProject()

        pluginProject.projectName = pyutProject.projectName
        pluginProject.fileName    = pyutProject.filename
        pluginProject.codePath    = pyutProject.codePath
        pluginProject.version     = OglVersion.version
        for document in pyutProject.documents:
            pyutDocument:   IPyutDocument = cast(IPyutDocument, document)
            pluginDocument: PluginDocument = PluginDocument()

            pluginDocument.documentType  = PluginDocumentType.toEnum(pyutDocument.diagramType.name)
            pluginDocument.documentTitle = PluginDocumentTitle(pyutDocument.title)

            diagramFrame: UmlFrameType = pyutDocument.diagramFrame
            scrollPosX, scrollPosY = diagramFrame.GetViewStart()
            xUnit, yUnit = diagramFrame.GetScrollPixelsPerUnit()

            pluginDocument.scrollPositionX = scrollPosX
            pluginDocument.scrollPositionY = scrollPosY
            pluginDocument.pixelsPerUnitX  = xUnit
            pluginDocument.pixelsPerUnitY  = yUnit

            for umlObject in diagramFrame.umlObjects:
                match umlObject:
                    case OglInterface2():
                        oglInterface2: OglInterface2 = cast(OglInterface2, umlObject)
                        pluginDocument.oglLinks.append(oglInterface2)
                    case OglSDInstance():
                        oglSDInstance: OglSDInstance = cast(OglSDInstance, umlObject)
                        pluginDocument.oglSDInstances[oglSDInstance.pyutObject.id] = oglSDInstance
                    case OglSDMessage():
                        oglSDMessage: OglSDMessage = cast(OglSDMessage, umlObject)
                        pluginDocument.oglSDMessages[oglSDMessage.pyutObject.id] = oglSDMessage
                    case OglClass():
                        pluginDocument.oglClasses.append(umlObject)
                    case OglLink():
                        pluginDocument.oglLinks.append(umlObject)
                    case OglNote():
                        pluginDocument.oglNotes.append(umlObject)
                    case OglText():
                        pluginDocument.oglTexts.append(umlObject)
                    case OglActor():
                        pluginDocument.oglActors.append(umlObject)
                    case OglUseCase():
                        pluginDocument.oglUseCases.append(umlObject)
                    case _:
                        self.logger.error(f'Unknown umlObject: {umlObject=}')

            pluginProject.pluginDocuments[pluginDocument.documentTitle] = pluginDocument

        return pluginProject
