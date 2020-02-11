
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
from org.pyut.ogl.OglAssociation import CENTER
from org.pyut.ogl.OglAssociation import DEST_CARD
from org.pyut.ogl.OglAssociation import OglAssociation
from org.pyut.ogl.OglAssociation import SRC_CARD
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglUseCase import OglUseCase

from org.pyut.ogl.sd.OglSDInstance import OglSDInstance
from org.pyut.ogl.sd.OglSDMessage import OglSDMessage

from org.pyut.PyutSDInstance import PyutSDInstance
from org.pyut.PyutSDMessage import PyutSDMessage

# from org.pyut.PyutClass import PyutClass
from org.pyut.PyutField import PyutField
from org.pyut.PyutMethod import PyutMethod
from org.pyut.PyutNote import PyutNote
from org.pyut.PyutLink import PyutLink
from org.pyut.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.PyutConstants import PyutConstants
from org.pyut.PyutUtils import PyutUtils

from org.pyut.persistence.converters.ToOgl import OglActors
from org.pyut.persistence.converters.ToOgl import OglObjects
from org.pyut.persistence.converters.ToOgl import OglSDInstances
from org.pyut.persistence.converters.ToOgl import OglSDMessages
from org.pyut.persistence.converters.ToOgl import OglUseCases

from org.pyut.persistence.converters.ToOgl import ToOgl
from org.pyut.persistence.converters.ToPyutXml import ToPyutXml

from org.pyut.persistence.converters.ToOgl import OglLinks
from org.pyut.persistence.converters.ToOgl import OglClasses
from org.pyut.persistence.converters.ToOgl import OglNotes
from org.pyut.persistence.converters.PyutXmlConstants import PyutXmlConstants
from org.pyut.persistence.converters.IDFactorySingleton import IDFactory

from org.pyut.ui.PyutDocument import PyutDocument
from org.pyut.ui.PyutProject import PyutProject

from org.pyut.general.Mediator import getMediator
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
    DOCUMENT_ATTR_TITLE:    str = 'title'
    DOCUMENT_ATTR_DOC_TYPE: str = 'type'
    _idFactory: IDFactory = IDFactory()
    """
    Temporarily make this a class variable until I get everything moved to the new `ToPyutXml'
    This makes it accessible to both 
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

        Returns:  And minidom XML Document
        """
        dlg:    Dialog   = Dialog(None, -1, "Saving...", style=STAY_ON_TOP | ICON_INFORMATION | RESIZE_BORDER, size=Size(207, 70))
        xmlDoc: Document = Document()
        try:
            # xmlDoc: Document  = Document()
            top     = xmlDoc.createElement("PyutProject")
            top.setAttribute('version', str(PyutXml.VERSION))
            top.setAttribute('CodePath', project.getCodePath())

            xmlDoc.appendChild(top)

            gauge = Gauge(dlg, -1, 100, pos=Point(2, 5), size=Size(200, 30))
            dlg.Show(True)
            wxYield()

            toPyutXml: ToPyutXml = ToPyutXml()
            # Save all documents in the project
            for document in project.getDocuments():

                document: PyutDocument = cast(PyutDocument, document)

                documentNode = xmlDoc.createElement("PyutDocument")

                docType: str = document.getType().__str__()

                documentNode.setAttribute(PyutXml.DOCUMENT_ATTR_DOC_TYPE, docType)
                documentNode.setAttribute(PyutXml.DOCUMENT_ATTR_TITLE, document.title)
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
                        documentNode.appendChild(self._OglNote2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglActor):
                        documentNode.appendChild(self._OglActor2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglUseCase):
                        documentNode.appendChild(self._OglUseCase2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglSDInstance):
                        documentNode.appendChild(self._OglSDInstance2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglSDMessage):
                        documentNode.appendChild(self._OglSDMessage2xml(oglObject, xmlDoc))
                    # OglLink comes last because OglSDInstance is a subclass of OglLink
                    # Now I know why OglLink used to double inherit from LineShape, ShapeEventHandler
                    # I changed it to inherit from OglLink directly
                    elif isinstance(oglObject, OglLink):
                        documentNode.appendChild(self._OglLink2xml(oglObject, xmlDoc))
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
            toOgl: ToOgl = ToOgl()
            for documentNode in dom.getElementsByTagName("PyutDocument"):

                documentNode: Element = cast(Element, documentNode)
                docTypeStr:   str     = documentNode.getAttribute(PyutXml.DOCUMENT_ATTR_DOC_TYPE)
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

    def _PyutSDInstance2xml(self, pyutSDInstance: PyutSDInstance, xmlDoc: Document):
        """
        Exporting an PyutSDInstance to an miniDom Element.

        @param  pyutSDInstance : Class to save
        @param xmlDoc : xml document
        @return Element : XML Node
        """
        root = xmlDoc.createElement('SDInstance')
        eltId = self._idFactory.getID(pyutSDInstance)

        root.setAttribute('id',           str(eltId))
        root.setAttribute('instanceName', pyutSDInstance.getInstanceName())
        root.setAttribute('lifeLineLength', str(pyutSDInstance.getInstanceLifeLineLength()))
        return root

    def _OglSDInstance2xml(self, oglSDInstance, xmlDoc):
        """
        Exporting an OglSDInstance to a miniDom Element.

        @param OglSDInstance oglSDInstance : Instance to save
        @param xmlDoc : xml document
        @return Element : XML Node
        """
        root = xmlDoc.createElement('GraphicSDInstance')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglSDInstance, root)

        # adding the data layer object
        root.appendChild(self._PyutSDInstance2xml(oglSDInstance.getPyutObject(), xmlDoc))

        return root

    def _PyutSDMessage2xml(self, pyutSDMessage: PyutSDMessage, xmlDoc: Document):
        """
        Exporting an PyutSDMessage to an miniDom Element.

        @param pyutSDMessage : SDMessage to save
        @param xmlDoc : xml document
        @return Element : XML Node
        """
        root = xmlDoc.createElement('SDMessage')

        # ID
        eltId = self._idFactory.getID(pyutSDMessage)
        root.setAttribute('id', str(eltId))

        # message
        root.setAttribute('message', pyutSDMessage.getMessage())

        # time
        idSrc = self._idFactory.getID(pyutSDMessage.getSource())
        idDst = self._idFactory.getID(pyutSDMessage.getDest())
        root.setAttribute('srcTime', str(pyutSDMessage.getSrcTime()))
        root.setAttribute('dstTime', str(pyutSDMessage.getDstTime()))
        root.setAttribute('srcID', str(idSrc))
        root.setAttribute('dstID', str(idDst))

        return root

    def _OglSDMessage2xml(self, oglSDMessage, xmlDoc):
        """
        Exporting an OglSDMessage to an miniDom Element.

        @param oglSDMessage : Message to save
        @param xmlDoc
        @return Element : XML Node
        """
        root = xmlDoc.createElement('GraphicSDMessage')

        # adding the data layer object
        root.appendChild(self._PyutSDMessage2xml(oglSDMessage.getPyutObject(), xmlDoc))

        return root

    # def _PyutField2xml(self, pyutField, xmlDoc):
    #     """
    #     Exporting a PyutField to an miniDom Element
    #
    #     @param PyutField pyutField : Field to save
    #     @param xmlDoc xmlDoc : xml document
    #     @return Element : XML Node
    #     """
    #     root = xmlDoc.createElement('Field')
    #
    #     # adding the parent XML
    #     # pyutField is a param
    #     root.appendChild(self._PyutParam2xml(pyutField, xmlDoc))
    #
    #     # field visibility
    #     root.setAttribute('visibility', str(pyutField.getVisibility()))
    #
    #     return root
    #
    def _PyutParam2xml(self, pyutParam, xmlDoc):
        """
        Exporting a PyutParam to an miniDom Element.

        @param pyutParam : Parameters to save
        @param xmlDoc  : xml document
        @return Element : XML Node
        """
        root = xmlDoc.createElement('Param')

        # param name
        root.setAttribute('name', pyutParam.getName())

        # param type
        root.setAttribute('type', str(pyutParam.getType()))

        # param default value
        defaultValue = pyutParam.getDefaultValue()
        if defaultValue is not None:
            root.setAttribute('defaultValue', defaultValue)

        return root

    def _PyutLink2xml(self, pyutLink, xmlDoc):
        """
        Exporting an PyutLink to a miniDom Element.

        @param PyutLink pyutLink : Link to save
        @param xmlDoc : xml document
        @return Element : XML Node
        """

        root = xmlDoc.createElement('Link')
        # link name
        root.setAttribute('name', pyutLink.getName())

        # link type
        root.setAttribute('type', pyutLink.getType().name)

        root.setAttribute('cardSrc',         pyutLink.sourceCardinality)        # link cardinality source
        root.setAttribute('cardDestination', pyutLink.destinationCardinality)   # link cardinality destination

        # link bidir
        root.setAttribute('bidir', str(pyutLink.getBidir()))

        # link source
        srcLinkId = self._idFactory.getID(pyutLink.getSource())
        root.setAttribute('sourceId', str(srcLinkId))

        # link destination
        destLinkId = self._idFactory.getID(pyutLink.getDestination())
        root.setAttribute('destId', str(destLinkId))

        return root

    # def _PyutMethod2xml(self, pyutMethod, xmlDoc):
    #     """
    #     Exporting an PyutMethod to an miniDom Element.
    #
    #     @param PyutMethod pyutMethod : Method to save
    #     @param xmlDoc : xml document
    #     @return Element : XML Node
    #     """
    #     root = xmlDoc.createElement('Method')
    #
    #     # method name
    #     root.setAttribute('name', pyutMethod.getName())
    #
    #     # method visibility
    #     visibility: PyutVisibilityEnum = pyutMethod.getVisibility()
    #     visStr: str = visibility.__str__()
    #     if visibility is not None:
    #         root.setAttribute('visibility', visStr)
    #
    #     # for all modifiers
    #     for modifier in pyutMethod.getModifiers():
    #         xmlModifier = xmlDoc.createElement('Modifier')
    #         xmlModifier.setAttribute('name', modifier.getName())
    #         root.appendChild(xmlModifier)
    #
    #     # method return type
    #     returnType = pyutMethod.getReturns()
    #     if returnType is not None:
    #         xmlReturnType = xmlDoc.createElement('Return')
    #         xmlReturnType.setAttribute('type', str(returnType))
    #         root.appendChild(xmlReturnType)
    #
    #     # method params
    #     for param in pyutMethod.getParams():
    #         root.appendChild(self._PyutParam2xml(param, xmlDoc))
    #
    #     return root

    # def _PyutClass2xml(self, pyutClass: PyutClass, xmlDoc: Document):
    #     """
    #     Exporting an PyutClass to an miniDom Element.
    #
    #     @param  pyutClass : Class to save
    #
    #     @param xmlDoc : xml document
    #
    #     @return Element : XML Node
    #     """
    #     root = xmlDoc.createElement('Class')
    #
    #     # ID
    #     classId = self._idFactory.getID(pyutClass)
    #     root.setAttribute('id', str(classId))
    #
    #     # class name
    #     root.setAttribute('name', pyutClass.getName())
    #
    #     # class stereotype
    #     stereotype = pyutClass.getStereotype()
    #     if stereotype is not None:
    #         root.setAttribute('stereotype', stereotype.getStereotype())
    #
    #     root.setAttribute('description', pyutClass.getDescription())
    #     root.setAttribute('filename', pyutClass.getFilename())
    #     root.setAttribute('showMethods', str(pyutClass.getShowMethods()))
    #     root.setAttribute('showFields',  str(pyutClass.getShowFields()))
    #     root.setAttribute('showStereotype', str(pyutClass.getShowStereotype()))
    #
    #     # methods
    #     for method in pyutClass.getMethods():
    #         root.appendChild(self._PyutMethod2xml(method, xmlDoc))
    #
    #     # fields
    #     for field in pyutClass.getFields():
    #         root.appendChild(self._PyutField2xml(field, xmlDoc))
    #
    #     return root

    def _PyutNote2xml(self, pyutNote, xmlDoc):
        """
        Exporting an PyutNote to an miniDom Element.

        @param pyutNote : Note to convert
        @param xmlDoc : xml document
        @return Element          : New miniDom element
        """
        root = xmlDoc.createElement('Note')
        # ID
        noteId = self._idFactory.getID(pyutNote)
        root.setAttribute('id', str(noteId))

        # Note
        name = pyutNote.getName()
        name = name.replace('\n', "\\\\\\\\")
        root.setAttribute('name', name)
        root.setAttribute('filename', pyutNote.getFilename())

        return root

    def _PyutActor2xml(self, pyutActor, xmlDoc):
        """
        Exporting an PyutActor to an miniDom Element.

        @param PyutNote pyutActor : Note to convert
        @param xmlDoc : xml document
        @return Element : New miniDom element
        """
        root = xmlDoc.createElement('Actor')

        actorId = self._idFactory.getID(pyutActor)
        root.setAttribute('id', str(actorId))
        root.setAttribute('name', pyutActor.getName())
        root.setAttribute('filename', pyutActor.getFilename())

        return root

    def _PyutUseCase2xml(self, pyutUseCase, xmlDoc):
        """
        Exporting an PyutUseCase to a miniDom Element.

        @param PyutNote pyutUseCase : Note to convert
        @param xmlDoc xmlDoc : xml document
        @return Element : New miniDom element
        """
        root = xmlDoc.createElement('UseCase')

        useCaseId = self._idFactory.getID(pyutUseCase)
        root.setAttribute('id', str(useCaseId))

        # Note
        root.setAttribute('name', pyutUseCase.getName())

        # filename (lb@alawa.ch)
        root.setAttribute('filename', pyutUseCase.getFilename())

        return root

    def _appendOglBase(self, oglObject, root):
        """
        Saves the position and size of the OGL object in XML node.

        @param OglObject oglObject : OGL Object
        @param Element root : XML node to write
        """
        # Saving size
        w, h = oglObject.GetModel().GetSize()
        root.setAttribute('width', str(float(w)))
        root.setAttribute('height', str(float(h)))

        # Saving position
        x, y = oglObject.GetModel().GetPosition()
        root.setAttribute('x', str(x))
        root.setAttribute('y', str(y))

    def _OglLink2xml(self, oglLink: OglLink, xmlDoc: Document):
        """
        """
        root = xmlDoc.createElement('GraphicLink')

        # Append OGL object base
        # save src and dst anchor points
        x, y = oglLink.GetSource().GetModel().GetPosition()
        root.setAttribute('srcX', str(x))
        root.setAttribute('srcY', str(y))

        x, y = oglLink.GetDestination().GetModel().GetPosition()
        root.setAttribute('dstX', str(x))
        root.setAttribute('dstY', str(y))

        root.setAttribute('spline', str(oglLink.GetSpline()))

        if isinstance(oglLink, OglAssociation):

            center = oglLink.getLabels()[CENTER]
            src = oglLink.getLabels()[SRC_CARD]
            dst = oglLink.getLabels()[DEST_CARD]

            label = xmlDoc.createElement("LabelCenter")
            root.appendChild(label)
            x, y = center.GetModel().GetPosition()
            label.setAttribute("x", str(x))
            label.setAttribute("y", str(y))

            label = xmlDoc.createElement("LabelSrc")
            root.appendChild(label)
            x, y = src.GetModel().GetPosition()
            label.setAttribute("x", str(x))
            label.setAttribute("y", str(y))
            label = xmlDoc.createElement("LabelDst")
            root.appendChild(label)
            x, y = dst.GetModel().GetPosition()
            label.setAttribute("x", str(x))
            label.setAttribute("y", str(y))

        # save control points (not anchors!)
        for x, y in oglLink.GetSegments()[1:-1]:
            item = xmlDoc.createElement('ControlPoint')
            item.setAttribute('x', str(x))
            item.setAttribute('y', str(y))
            root.appendChild(item)

        # adding the data layer object
        root.appendChild(self._PyutLink2xml(oglLink.getPyutObject(), xmlDoc))

        return root

    # def _OglClass2xml(self, oglClass: OglClass, xmlDoc: Document):
    #     """
    #     Exporting an OglClass to an miniDom Element.
    #
    #     @param  oglClass : Class to save
    #     @param xmlDoc xmlDoc : xml document
    #     @return Element : XML Node
    #     """
    #     root = xmlDoc.createElement('GraphicClass')
    #
    #     # Append OGL object base (size and pos)
    #     self._appendOglBase(oglClass, root)
    #
    #     # adding the data layer object
    #     root.appendChild(self._PyutClass2xml(oglClass.getPyutObject(), xmlDoc))
    #
    #     return root

    def _OglNote2xml(self, oglNote, xmlDoc):
        """
        Exporting an OglNote to an miniDom Element.

        @param OglNote oglNote : Note to convert
        @param xmlDoc xmlDoc : xml document

        @return Element        : New miniDom element
        """
        root = xmlDoc.createElement('GraphicNote')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglNote, root)

        # adding the data layer object
        root.appendChild(self._PyutNote2xml(oglNote.getPyutObject(), xmlDoc))

        return root

    def _OglActor2xml(self, oglActor, xmlDoc):
        """
        Exporting an OglActor to an miniDom Element.

        @param OglActor oglActor : Actor to convert
        @param xmlDoc xmlDoc : xml document
        @return Element : New miniDom element
        """
        root = xmlDoc.createElement('GraphicActor')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglActor, root)

        # adding the data layer object
        root.appendChild(self._PyutActor2xml(oglActor.getPyutObject(), xmlDoc))

        return root

    def _OglUseCase2xml(self, oglUseCase, xmlDoc):
        """
        Exporting an OglUseCase to an miniDom Element.

        @param oglUseCase : UseCase to convert
        @param xmlDoc xmlDoc : xml document
        @return Element : New miniDom element

        """
        root = xmlDoc.createElement('GraphicUseCase')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglUseCase, root)

        # adding the data layer object
        root.appendChild(self._PyutUseCase2xml(oglUseCase.getPyutObject(), xmlDoc))

        return root

    def _getControlPoints(self, link):
        """
        To extract control points from links.

        Python 3:  This method does not seem to be used;  I'll comment it out and raise an
        exception;  Especially, since I don't know where the `Class` class comes
        from == hasii
        """
        raise NotImplementedError('I guess this method is used after all.  See the comments')
        # class methods for this current class
        # allControlPoints = []
        #
        # for cp in Class.getElementsByTagName('ControlPoint'):
        #
        #     # point position
        #     x = cp.getAttribute('x')
        #     y = cp.getAttribute('y')
        #
        #     point = ControlPoint(x, y)
        #     allControlPoints.append(point)
        #
        # return allControlPoints

    def __renderClassDiagram(self, documentNode: Element, toOgl: ToOgl, umlFrame: UmlFrame):
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

    def __renderUseCaseDiagram(self, documentNode: Element, toOgl: ToOgl, umlFrame: UmlFrame):
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
        self._displayTheSDMessages(oglSDMessages, umlFrame)

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

    def _displayTheSDMessages(self, oglSDMessages: OglSDMessages, umlFrame: UmlFrame):
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
        root: Element = dom.getElementsByTagName("PyutProject")[0]
        if root.hasAttribute('version'):
            version = int(root.getAttribute("version"))
        else:
            version = 1
        if version != PyutXml.VERSION:
            self.logger.error("Wrong version of the file loader")
            eMsg: str = f'This is version {PyutXml.VERSION} and the file version is {version}'
            self.logger.error(eMsg)
            raise Exception(f'VERSION_ERROR:  {eMsg}')

        return root

    def __determineDocumentTitle(self, documentNode) -> str:

        docTitle:   str = documentNode.getAttribute(PyutXml.DOCUMENT_ATTR_TITLE)
        docTypeStr: str = documentNode.getAttribute(PyutXml.DOCUMENT_ATTR_DOC_TYPE)

        if docTitle == '' or docTitle is None:
            return docTypeStr
        else:
            return docTitle

    def __showAppropriateUmlFrame(self, document) -> UmlFrame:

        umlFrame: UmlFrame = document.getFrame()
        ctrl = getMediator()
        ctrl.getFileHandling().showFrame(umlFrame)

        return umlFrame
