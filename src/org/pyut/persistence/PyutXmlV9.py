
from typing import List
from typing import cast

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
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
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglUseCase import OglUseCase

from org.pyut.ogl.sd.OglSDInstance import OglSDInstance
from org.pyut.ogl.sd.OglSDMessage import OglSDMessage

from org.pyut.PyutConstants import PyutConstants
from org.pyut.PyutUtils import PyutUtils

from org.pyut.persistence.converters.MiniDomToOgl import OglActors
from org.pyut.persistence.converters.MiniDomToOgl import OglObjects
from org.pyut.persistence.converters.MiniDomToOgl import OglSDInstances
from org.pyut.persistence.converters.MiniDomToOgl import OglSDMessages
from org.pyut.persistence.converters.MiniDomToOgl import OglUseCases
from org.pyut.persistence.converters.MiniDomToOgl import OglLinks
from org.pyut.persistence.converters.MiniDomToOgl import OglClasses
from org.pyut.persistence.converters.MiniDomToOgl import OglNotes

from org.pyut.persistence.converters.MiniDomToOgl import MiniDomToOgl
from org.pyut.persistence.converters.OglToMiniDom import OglToMiniDom


from org.pyut.persistence.converters.PyutXmlConstants import PyutXmlConstants

from org.pyut.ui.PyutDocument import PyutDocument
from org.pyut.ui.PyutProject import PyutProject

from org.pyut.general.Mediator import Mediator
from org.pyut.general.Globals import _

from org.pyut.ui.UmlFrame import UmlFrame


class PyutXml:

    VERSION: int = 9
    """
    Use this class to save and load a PyUT UML diagram in XML.
    This class offers two main methods.  They are:
    
     * `save()` 
     * `load()`
     
     
    Using the minidom API you can use the save method to get the
    diagram converted to its corresponding XML representation. For loading, you have to parse
    the XML file and indicate the UML frame onto which you want to draw
    (See `UmlFrame`).

    This module is dynamically loaded based on the input XML's version number.  This
    class supports `PyutXml.VERSION`  9
    
    """
    def __init__(self):
        """
        Constructor
        """
        self.logger: Logger = getLogger(__name__)

        # self._idFactory = IDFactory()

        self._dlgGauge: Dialog = cast(Dialog, None)

    def save(self, project: PyutProject) -> Document:
        """
        Save diagram in XML file.

        Args:
            project:  The project to write as XML

        Returns:
            A minidom XML Document
        """
        dlg:    Dialog   = Dialog(None, -1, "Saving...", style=STAY_ON_TOP | ICON_INFORMATION | RESIZE_BORDER, size=Size(207, 70))
        xmlDoc: Document = Document()
        try:
            # xmlDoc: Document  = Document()
            top     = xmlDoc.createElement(PyutXmlConstants.TOP_LEVEL_ELEMENT)
            top.setAttribute(PyutXmlConstants.ATTR_VERSION, str(PyutXml.VERSION))
            codePath: str = project.getCodePath()
            if codePath is None:
                top.setAttribute('CodePath', '')
            else:
                top.setAttribute('CodePath', codePath)

            xmlDoc.appendChild(top)

            gauge = Gauge(dlg, -1, 100, pos=Point(2, 5), size=Size(200, 30))
            dlg.Show(True)
            wxYield()

            toPyutXml: OglToMiniDom = OglToMiniDom()
            # Save all documents in the project
            for document in project.getDocuments():

                document: PyutDocument = cast(PyutDocument, document)

                documentNode = xmlDoc.createElement(PyutXmlConstants.ELEMENT_DOCUMENT)

                docType: str = document.getType().__str__()

                documentNode.setAttribute(PyutXmlConstants.ATTR_TYPE, docType)
                documentNode.setAttribute(PyutXmlConstants.ATTR_TITLE, document.title)
                top.appendChild(documentNode)

                oglObjects: List[OglObject] = document.getFrame().getUmlObjects()
                for i in range(len(oglObjects)):
                    gauge.SetValue(i * 100 / len(oglObjects))
                    wxYield()
                    oglObject = oglObjects[i]
                    if isinstance(oglObject, OglClass):
                        # documentNode.appendChild(self._OglClass2xml(oglObject, xmlDoc))
                        classElement: Element = toPyutXml.oglClassToXml(oglObject, xmlDoc)
                        documentNode.appendChild(classElement)
                    elif isinstance(oglObject, OglNote):
                        # documentNode.appendChild(self._OglNote2xml(oglObject, xmlDoc))
                        noteElement: Element = toPyutXml.oglNoteToXml(oglObject, xmlDoc)
                        documentNode.appendChild(noteElement)
                    elif isinstance(oglObject, OglActor):
                        # documentNode.appendChild(self._OglActor2xml(oglObject, xmlDoc))
                        actorElement: Element = toPyutXml.oglActorToXml(oglObject, xmlDoc)
                        documentNode.appendChild(actorElement)
                    elif isinstance(oglObject, OglUseCase):
                        # documentNode.appendChild(self._OglUseCase2xml(oglObject, xmlDoc))
                        useCaseElement: Element = toPyutXml.oglUseCaseToXml(oglObject, xmlDoc)
                        documentNode.appendChild(useCaseElement)
                    elif isinstance(oglObject, OglSDInstance):
                        # documentNode.appendChild(self._OglSDInstance2xml(oglObject, xmlDoc))
                        sdInstanceElement: Element = toPyutXml.oglSDInstanceToXml(oglObject, xmlDoc)
                        documentNode.appendChild(sdInstanceElement)
                    elif isinstance(oglObject, OglSDMessage):
                        # documentNode.appendChild(self._OglSDMessage2xml(oglObject, xmlDoc))
                        sdMessageElement: Element = toPyutXml.oglSDMessageToXml(oglObject, xmlDoc)
                        documentNode.appendChild(sdMessageElement)
                    # OglLink comes last because OglSDInstance is a subclass of OglLink
                    # Now I know why OglLink used to double inherit from LineShape, ShapeEventHandler
                    # I changed it to inherit from OglLink directly
                    elif isinstance(oglObject, OglLink):
                        # documentNode.appendChild(self._OglLink2xml(oglObject, xmlDoc))
                        linkElement: Element = toPyutXml.oglLinkToXml(oglObject, xmlDoc)
                        documentNode.appendChild(linkElement)
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
        umlFrame: UmlFrame = cast(UmlFrame, None)  # avoid Pycharm warning
        root = self.__validateXmlVersion(dom)
        try:
            project.setCodePath(root.getAttribute("CodePath"))
            self.__updateProgressDialog(newMessage='Reading elements...', newGaugeValue=1)
            toOgl: MiniDomToOgl = MiniDomToOgl()
            for documentNode in dom.getElementsByTagName(PyutXmlConstants.ELEMENT_DOCUMENT):

                documentNode: Element = cast(Element, documentNode)
                docTypeStr:   str     = documentNode.getAttribute(PyutXmlConstants.ATTR_TYPE)
                self.__updateProgressDialog(newMessage=f'Determine Title for document type: {docTypeStr}', newGaugeValue=2)

                docType:  DiagramType  = PyutConstants.diagramTypeFromString(docTypeStr)
                document: PyutDocument = project.newDocument(docType)
                document.title = self.__determineDocumentTitle(documentNode)

                umlFrame: UmlFrame = self.__showAppropriateUmlFrame(document)

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

    def __renderClassDiagram(self, documentNode: Element, toOgl: MiniDomToOgl, umlFrame: UmlFrame):
        """

        Args:
            documentNode:   A minidom document element
            toOgl:          The converter class
            umlFrame:       Where to render
        """
        oglClasses: OglClasses = toOgl.getOglClasses(documentNode.getElementsByTagName(PyutXmlConstants.ELEMENT_GRAPHIC_CLASS))
        oglNotes:   OglNotes   = toOgl.getOglNotes(documentNode.getElementsByTagName('GraphicNote'))

        mergedOglObjects: OglObjects = cast(OglObjects, oglClasses.copy())
        mergedOglObjects.update(oglNotes)

        self.__displayTheClasses(oglClasses, umlFrame)
        oglLinks: OglLinks = toOgl.getOglLinks(documentNode.getElementsByTagName("GraphicLink"), mergedOglObjects)
        self.__displayTheLinks(oglLinks, umlFrame)
        self.__displayTheNotes(oglNotes, umlFrame)

    def __renderUseCaseDiagram(self, documentNode: Element, toOgl: MiniDomToOgl, umlFrame: UmlFrame):
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

    def __displayTheClasses(self, oglClasses: OglClasses, umlFrame: UmlFrame):
        """
        Place the OGL classes on the input frame at their respective positions

        Args:
            oglClasses: A dictionary of OGL classes
            umlFrame:   The UML Frame to place the OGL objects on
        """
        for oglClass in oglClasses.values():
            self.__displayAnOglObject(oglClass, umlFrame)

    def __displayTheLinks(self, oglLinks: OglLinks, umlFrame: UmlFrame):
        """
        Place the OGL links on the input frame at their respective positions

        Args:
            oglLinks:   A dictionary of OGL links
            umlFrame:   The UML Frame to place the OGL objects on
        """
        for oglLink in oglLinks:
            umlFrame.GetDiagram().AddShape(oglLink, withModelUpdate=True)

    def __displayTheNotes(self, oglNotes: OglNotes, umlFrame: UmlFrame):
        for oglNote in oglNotes.values():
            self.__displayAnOglObject(oglNote, umlFrame)

    def __displayTheActors(self, oglActors: OglActors, umlFrame: UmlFrame):
        for oglActor in oglActors.values():
            self.__displayAnOglObject(oglActor, umlFrame)

    def __displayTheUseCases(self, oglUseCases: OglUseCases, umlFrame: UmlFrame):
        for oglUseCase in oglUseCases.values():
            self.__displayAnOglObject(oglUseCase, umlFrame)

    def __displayTheSDMessages(self, oglSDMessages: OglSDMessages, umlFrame: UmlFrame):
        for oglSDMessage in oglSDMessages.values():
            oglSDMessage: OglSDMessage = cast(OglSDMessage, oglSDMessage)
            umlFrame.getDiagram().AddShape(oglSDMessage)

    def __displayAnOglObject(self, oglObject: OglObject, umlFrame: UmlFrame):
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

    def __cleanupProgressDialog(self, umlFrame: UmlFrame):

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

    def __showAppropriateUmlFrame(self, document) -> UmlFrame:

        umlFrame: UmlFrame = document.getFrame()
        mediator: Mediator = Mediator()

        mediator.getFileHandling().showFrame(umlFrame)

        return umlFrame
