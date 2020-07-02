from typing import Dict
from typing import List

from typing import cast

from logging import Logger
from logging import getLogger

# noinspection PyUnresolvedReferences
from xml.dom.minidom import Document
# noinspection PyUnresolvedReferences
from xml.dom.minidom import Element

from wx import Dialog
from wx import Gauge
from wx import Point
from wx import Size
from wx import Yield as wxYield

from wx import ICON_INFORMATION
from wx import RESIZE_BORDER
from wx import STAY_ON_TOP
from wx import ID_ANY

from org.pyut.enums.DiagramType import DiagramType

from org.pyut.ogl.OglActor import OglActor
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglInterface2 import OglInterface2
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglUseCase import OglUseCase

from org.pyut.ogl.sd.OglSDInstance import OglSDInstance
from org.pyut.ogl.sd.OglSDMessage import OglSDMessage

from org.pyut.PyutConstants import PyutConstants
from org.pyut.PyutUtils import PyutUtils

from org.pyut.persistence.converters.MiniDomToOglV10 import OglActors
from org.pyut.persistence.converters.MiniDomToOglV10 import OglObjects
from org.pyut.persistence.converters.MiniDomToOglV10 import OglSDInstances
from org.pyut.persistence.converters.MiniDomToOglV10 import OglSDMessages
from org.pyut.persistence.converters.MiniDomToOglV10 import OglUseCases
from org.pyut.persistence.converters.MiniDomToOglV10 import OglLinks
from org.pyut.persistence.converters.MiniDomToOglV10 import OglClasses
from org.pyut.persistence.converters.MiniDomToOglV10 import OglNotes
from org.pyut.persistence.converters.MiniDomToOglV10 import OglInterfaces

from org.pyut.persistence.converters.MiniDomToOglV10 import MiniDomToOgl as MiniDomToOglV10
from org.pyut.persistence.converters.OglToMiniDomV10 import OglToMiniDom as OglToMiniDomV10

from org.pyut.persistence.converters.PyutXmlConstants import PyutXmlConstants

from org.pyut.ui.PyutDocument import PyutDocument
from org.pyut.ui.PyutProject import PyutProject
from org.pyut.ui.UmlDiagramsFrame import UmlDiagramsFrame

from org.pyut.general.Mediator import getMediator
from org.pyut.general.Globals import _


class PyutXml:

    VERSION: int = 10
    """
    Use this class to save and load a PyUT UML diagram in XML.
    This class offers two main methods.  They are:
    
     * `save()` 
     * `load()`
     
     
    Using the minidom API you can use the save method to get the
    diagram converted to its corresponding XML representation. For loading, you have to parse
    the XML file and indicate the UML frame onto which you want to draw
    (See `UmlDiagramsFrame`).

    This module is dynamically loaded based on the input XML's version number.  This
    class supports `PyutXml.VERSION`  10
    
    """
    def __init__(self):
        """
        Constructor
        """
        self.logger: Logger = getLogger(__name__)
        self._dlgGauge: Dialog = cast(Dialog, None)

    def save(self, project: PyutProject) -> Document:
        """
        Save diagram in XML file.

        Args:
            project:  The project to write as XML

        Returns:
            A minidom XML Document
        """
        assert project is not None, 'Oops someone sent me a bad project'

        dlg:    Dialog   = Dialog(None, ID_ANY, "Saving...", style=STAY_ON_TOP | ICON_INFORMATION | RESIZE_BORDER, size=Size(207, 70))
        xmlDoc: Document = Document()
        try:
            top = xmlDoc.createElement(PyutXmlConstants.TOP_LEVEL_ELEMENT)
            top.setAttribute(PyutXmlConstants.ATTR_VERSION, str(PyutXml.VERSION))
            codePath: str = project.getCodePath()
            if codePath is None:
                top.setAttribute(PyutXmlConstants.ATTR_CODE_PATH, '')
            else:
                top.setAttribute(PyutXmlConstants.ATTR_CODE_PATH, codePath)

            xmlDoc.appendChild(top)

            gauge = Gauge(dlg, ID_ANY, 100, pos=Point(2, 5), size=Size(200, 30))
            dlg.Show(True)
            wxYield()

            toPyutXml: OglToMiniDomV10 = OglToMiniDomV10()
            # Save all documents in the project
            for document in project.getDocuments():

                document:     PyutDocument = cast(PyutDocument, document)
                documentNode: Element      = self.__pyutDocumentToPyutXml(xmlDoc=xmlDoc, pyutDocument=document)

                top.appendChild(documentNode)

                oglObjects: List[OglObject] = document.getFrame().getUmlObjects()
                for i in range(len(oglObjects)):
                    gauge.SetValue(i * 100 / len(oglObjects))
                    wxYield()
                    oglObject = oglObjects[i]
                    if isinstance(oglObject, OglClass):
                        classElement: Element = toPyutXml.oglClassToXml(oglObject, xmlDoc)
                        documentNode.appendChild(classElement)
                    elif isinstance(oglObject, OglInterface2):
                        classElement: Element = toPyutXml.oglInterface2ToXml(oglObject, xmlDoc)
                        documentNode.appendChild(classElement)
                    elif isinstance(oglObject, OglNote):
                        noteElement: Element = toPyutXml.oglNoteToXml(oglObject, xmlDoc)
                        documentNode.appendChild(noteElement)
                    elif isinstance(oglObject, OglActor):
                        actorElement: Element = toPyutXml.oglActorToXml(oglObject, xmlDoc)
                        documentNode.appendChild(actorElement)
                    elif isinstance(oglObject, OglUseCase):
                        useCaseElement: Element = toPyutXml.oglUseCaseToXml(oglObject, xmlDoc)
                        documentNode.appendChild(useCaseElement)
                    elif isinstance(oglObject, OglSDInstance):
                        sdInstanceElement: Element = toPyutXml.oglSDInstanceToXml(oglObject, xmlDoc)
                        documentNode.appendChild(sdInstanceElement)
                    elif isinstance(oglObject, OglSDMessage):
                        sdMessageElement: Element = toPyutXml.oglSDMessageToXml(oglObject, xmlDoc)
                        documentNode.appendChild(sdMessageElement)
                    # OglLink comes last because OglSDInstance is a subclass of OglLink
                    # Now I know why OglLink used to double inherit from LineShape, ShapeEventHandler
                    # I changed it to inherit from OglLink directly
                    elif isinstance(oglObject, OglLink):
                        linkElement: Element = toPyutXml.oglLinkToXml(oglObject, xmlDoc)
                        documentNode.appendChild(linkElement)
                    else:
                        self.logger.warning(f'Unhandled OGL Object: {oglObject}')
        except (ValueError, Exception) as e:
            try:
                dlg.Destroy()
                self.logger.error(f'{e}')
            except (ValueError, Exception) as e:
                self.logger.error(f'{e}')
            PyutUtils.displayError(_("Can't save file"))
            return xmlDoc

        dlg.Destroy()

        return xmlDoc

    def open(self, dom: Document, project: PyutProject):
        """
        Open a file and create a diagram.

        Args:
            dom:        The minidom document
            project:    The UI Project to fill out
        """
        self.__setupProgressDialog()
        umlFrame: UmlDiagramsFrame = cast(UmlDiagramsFrame, None)  # avoid Pycharm warning
        root = self.__validateXmlVersion(dom)
        try:
            project.setCodePath(root.getAttribute("CodePath"))
            self.__updateProgressDialog(newMessage='Reading elements...', newGaugeValue=1)
            wxYield()
            toOgl: MiniDomToOglV10 = MiniDomToOglV10()
            for documentNode in dom.getElementsByTagName(PyutXmlConstants.ELEMENT_DOCUMENT):

                documentNode: Element = cast(Element, documentNode)
                docTypeStr:   str     = documentNode.getAttribute(PyutXmlConstants.ATTR_TYPE)
                self.__updateProgressDialog(newMessage=f'Determine Title for document type: {docTypeStr}', newGaugeValue=2)
                wxYield()

                docType:  DiagramType  = PyutConstants.diagramTypeFromString(docTypeStr)
                document: PyutDocument = project.newDocument(docType)
                document.title = self.__determineDocumentTitle(documentNode)

                umlFrame: UmlDiagramsFrame = self.__showAppropriateUmlFrame(document)
                self.__positionAndSetupDiagramFrame(umlFrame=umlFrame, documentNode=documentNode)

                self.__updateProgressDialog(newMessage='Start Conversion...', newGaugeValue=3)

                if docType == DiagramType.CLASS_DIAGRAM:
                    self.__renderClassDiagram(documentNode, toOgl, umlFrame)
                elif docType == DiagramType.USECASE_DIAGRAM:
                    self.__renderUseCaseDiagram(documentNode, toOgl, umlFrame)
                elif docType == DiagramType.SEQUENCE_DIAGRAM:
                    self.__renderSequenceDiagram(documentNode, toOgl, umlFrame)

                self.__updateProgressDialog(newMessage='Conversion Complete...', newGaugeValue=4)

        except (ValueError, Exception) as e:
            self._dlgGauge.Destroy()
            PyutUtils.displayError(_(f"Can not load file {e}"))
            umlFrame.Refresh()
            return

        self.__cleanupProgressDialog(umlFrame)

    def __pyutDocumentToPyutXml(self, xmlDoc: Document, pyutDocument: PyutDocument) -> Element:

        documentNode = xmlDoc.createElement(PyutXmlConstants.ELEMENT_DOCUMENT)

        docType: str = pyutDocument.getType().__str__()

        documentNode.setAttribute(PyutXmlConstants.ATTR_TYPE, docType)
        documentNode.setAttribute(PyutXmlConstants.ATTR_TITLE, pyutDocument.title)

        docFrame: UmlDiagramsFrame = pyutDocument.getFrame()
        scrollPosX, scrollPosY = docFrame.GetViewStart()
        documentNode.setAttribute(PyutXmlConstants.ATTR_SCROLL_POSITION_X, str(scrollPosX))
        documentNode.setAttribute(PyutXmlConstants.ATTR_SCROLL_POSITION_Y, str(scrollPosY))

        xUnit, yUnit = docFrame.GetScrollPixelsPerUnit()

        documentNode.setAttribute(PyutXmlConstants.ATTR_PIXELS_PER_UNIT_X, str(xUnit))
        documentNode.setAttribute(PyutXmlConstants.ATTR_PIXELS_PER_UNIT_Y, str(yUnit))

        return documentNode

    def __renderClassDiagram(self, documentNode: Element, toOgl: MiniDomToOglV10, umlFrame: UmlDiagramsFrame):
        """

        Args:
            documentNode:   A minidom document element
            toOgl:          The converter class
            umlFrame:       Where to render
        """
        oglClasses:    OglClasses    = toOgl.getOglClasses(documentNode.getElementsByTagName(PyutXmlConstants.ELEMENT_GRAPHIC_CLASS))
        oglNotes:      OglNotes      = toOgl.getOglNotes(documentNode.getElementsByTagName(PyutXmlConstants.ELEMENT_GRAPHIC_NOTE))
        oglInterfaces: OglInterfaces = toOgl.getOglInterfaces(documentNode.getElementsByTagName(PyutXmlConstants.ELEMENT_GRAPHIC_LOLLIPOP))

        mergedOglObjects: OglObjects = cast(OglObjects, oglClasses.copy())
        mergedOglObjects.update(oglNotes)

        self.__displayTheClasses(oglClasses, umlFrame)
        oglLinks: OglLinks = toOgl.getOglLinks(documentNode.getElementsByTagName(PyutXmlConstants.ELEMENT_GRAPHIC_LINK), mergedOglObjects)
        self.__displayTheLinks(oglLinks, umlFrame)
        self.__displayTheNotes(oglNotes, umlFrame)
        self.__displayTheInterfaces(oglInterfaces, umlFrame)

    def __renderUseCaseDiagram(self, documentNode: Element, toOgl: MiniDomToOglV10, umlFrame: UmlDiagramsFrame):
        """

        Args:
            documentNode:   A minidom document element
            toOgl:          The converter class
            umlFrame:       Where to render
        """
        oglObjects: OglObjects = cast(OglObjects, {})

        oglActors:   OglActors   = toOgl.getOglActors(documentNode.getElementsByTagName('GraphicActor'))
        oglUseCases: OglUseCases = toOgl.getOglUseCases(documentNode.getElementsByTagName('GraphicUseCase'))
        oglNotes:    OglNotes    = toOgl.getOglNotes(documentNode.getElementsByTagName('GraphicNote'))

        self.__displayTheActors(oglActors, umlFrame)
        self.__displayTheUseCases(oglUseCases, umlFrame)
        self.__displayTheNotes(oglNotes, umlFrame)

        mergedOglObjects: OglObjects = cast(OglObjects, oglObjects.copy())
        mergedOglObjects.update(oglActors)
        mergedOglObjects.update(oglNotes)
        mergedOglObjects.update(oglUseCases)

        oglLinks: OglLinks = toOgl.getOglLinks(documentNode.getElementsByTagName("GraphicLink"), mergedOglObjects)
        self.__displayTheLinks(oglLinks, umlFrame)

    def __renderSequenceDiagram(self, documentNode, toOgl, umlFrame):
        """

        Args:
            documentNode:   A minidom document element
            toOgl:          The converter class
            umlFrame:       Where to render
        """
        oglSDInstances: OglSDInstances = toOgl.getOglSDInstances(documentNode.getElementsByTagName("GraphicSDInstance"), umlFrame)
        oglSDMessages: OglSDMessages = toOgl.getOglSDMessages(documentNode.getElementsByTagName("GraphicSDMessage"), oglSDInstances)
        self.__displayTheSDMessages(oglSDMessages, umlFrame)

    def __displayTheClasses(self, oglClasses: OglClasses, umlFrame: UmlDiagramsFrame):
        """
        Place the OGL classes on the input frame at their respective positions

        Args:
            oglClasses: A dictionary of OGL classes
            umlFrame:   The UML Frame to place the OGL objects on
        """
        for oglClass in oglClasses.values():
            self.__displayAnOglObject(oglClass, umlFrame)

    def __displayTheInterfaces(self, oglInterfaces: OglInterfaces, umlFrame: UmlDiagramsFrame):

        for oglInterface in oglInterfaces:

            attachmentAnchor = oglInterface.destinationAnchor
            x, y = attachmentAnchor.GetPosition()

            umlFrame.addShape(oglInterface, x, y, withModelUpdate=True)

    def __displayTheLinks(self, oglLinks: OglLinks, umlFrame: UmlDiagramsFrame):
        """
        Place the OGL links on the input frame at their respective positions

        Args:
            oglLinks:   A dictionary of OGL links
            umlFrame:   The UML Frame to place the OGL objects on
        """
        for oglLink in oglLinks:
            umlFrame.GetDiagram().AddShape(oglLink, withModelUpdate=True)

    def __displayTheNotes(self, oglNotes: OglNotes, umlFrame: UmlDiagramsFrame):
        for oglNote in oglNotes.values():
            self.__displayAnOglObject(oglNote, umlFrame)

    def __displayTheActors(self, oglActors: OglActors, umlFrame: UmlDiagramsFrame):
        for oglActor in oglActors.values():
            self.__displayAnOglObject(oglActor, umlFrame)

    def __displayTheUseCases(self, oglUseCases: OglUseCases, umlFrame: UmlDiagramsFrame):
        for oglUseCase in oglUseCases.values():
            self.__displayAnOglObject(oglUseCase, umlFrame)

    def __displayTheSDMessages(self, oglSDMessages: OglSDMessages, umlFrame: UmlDiagramsFrame):
        for oglSDMessage in oglSDMessages.values():
            oglSDMessage: OglSDMessage = cast(OglSDMessage, oglSDMessage)
            umlFrame.getDiagram().AddShape(oglSDMessage)

    def __displayAnOglObject(self, oglObject: OglObject, umlFrame: UmlDiagramsFrame):
        x, y = oglObject.GetPosition()
        umlFrame.addShape(oglObject, x, y)

    def __setupProgressDialog(self):

        self._dlgGauge = Dialog(None, ID_ANY, "Loading...", style=STAY_ON_TOP | ICON_INFORMATION | RESIZE_BORDER, size=Size(250, 70))
        self._gauge: Gauge = Gauge(self._dlgGauge, ID_ANY, 5, pos=Point(2, 5), size=Size(200, 30))
        self._dlgGauge.Show(True)
        wxYield()

    def __updateProgressDialog(self, newMessage: str, newGaugeValue: int):

        self._dlgGauge.SetTitle(newMessage)
        self._gauge.SetValue(newGaugeValue)
        wxYield()

    def __cleanupProgressDialog(self, umlFrame: UmlDiagramsFrame):

        umlFrame.Refresh()
        self._gauge.SetValue(5)
        wxYield()
        self._dlgGauge.Destroy()

    def __validateXmlVersion(self, dom: Document) -> Element:
        """

        Args:
            dom: The minidom Document

        Returns:
            The root element unless the XML version is incorrect
        """
        root: Element = dom.getElementsByTagName(PyutXmlConstants.TOP_LEVEL_ELEMENT)[0]
        if root.hasAttribute(PyutXmlConstants.ATTR_VERSION):
            version = int(root.getAttribute(PyutXmlConstants.ATTR_VERSION))
        else:
            version = 1
        if version != PyutXml.VERSION:
            self.logger.error("Wrong version of the file loader")
            eMsg: str = f'This is version {PyutXml.VERSION} and the file version is {version}'
            self.logger.error(eMsg)
            raise Exception(f'VERSION_ERROR:  {eMsg}')

        return root

    def __determineDocumentTitle(self, documentNode) -> str:

        docTitle:   str = documentNode.getAttribute(PyutXmlConstants.ATTR_TITLE)
        docTypeStr: str = documentNode.getAttribute(PyutXmlConstants.ATTR_TYPE)

        if docTitle == '' or docTitle is None:
            return docTypeStr
        else:
            return docTitle

    def __showAppropriateUmlFrame(self, document) -> UmlDiagramsFrame:

        umlFrame: UmlDiagramsFrame = document.getFrame()
        ctrl = getMediator()
        ctrl.getFileHandling().showFrame(umlFrame)

        return umlFrame

    def __positionAndSetupDiagramFrame(self, umlFrame: UmlDiagramsFrame, documentNode: Element, ):

        xStr: str = documentNode.getAttribute(PyutXmlConstants.ATTR_SCROLL_POSITION_X)
        yStr: str = documentNode.getAttribute(PyutXmlConstants.ATTR_SCROLL_POSITION_Y)

        scrollPosX: int = PyutUtils.secureInteger(xStr)
        scrollPosY: int = PyutUtils.secureInteger(yStr)

        umlFrame.Scroll(scrollPosX, scrollPosY)

        xPerUnitStr: str = documentNode.getAttribute(PyutXmlConstants.ATTR_PIXELS_PER_UNIT_X)
        yPerUnitStr: str = documentNode.getAttribute(PyutXmlConstants.ATTR_PIXELS_PER_UNIT_Y)

        pixelsPerUnitX: int = PyutUtils.secureInteger(xPerUnitStr)
        pixelsPerUnitY: int = PyutUtils.secureInteger(yPerUnitStr)
        if pixelsPerUnitX != 0 and pixelsPerUnitY != 0:
            umlFrame.SetScrollRate(xstep=pixelsPerUnitX, ystep=pixelsPerUnitY)

    def _nonEmptyParameters(self, params: Dict[str, str]) -> bool:
        """

        Args:
            params: A dictionary where the key is the name of the value and the value is the value

        Returns:    `True` if all the parameters are valid else `False`
        """
        areValid: bool = True
        for paramName in params.keys():
            if self._isNoneEmptyParameter(params[paramName]):
                continue
            else:
                areValid = False
                self.logger.info(f'Parameter: {paramName} is either `None` or empty')

        return areValid

    def _isNoneEmptyParameter(self, valueToValidate: str):

        isValid: bool = True

        if valueToValidate is None or valueToValidate == '':
            isValid = False

        return isValid
