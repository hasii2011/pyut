
from typing import cast
from typing import Dict
from typing import List
from typing import Union
from typing import NewType

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Element
from xml.dom.minidom import NodeList

from org.pyut.miniogl.ControlPoint import ControlPoint
from org.pyut.miniogl.SelectAnchorPoint import SelectAnchorPoint

from org.pyut.enums.AttachmentPoint import AttachmentPoint

from org.pyut.model.PyutActor import PyutActor
from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutDisplayParameters import PyutDisplayParameters
from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutInterface import PyutInterface
from org.pyut.model.PyutLink import PyutLink
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutNote import PyutNote
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutSDInstance import PyutSDInstance
from org.pyut.model.PyutSDMessage import PyutSDMessage
from org.pyut.model.PyutType import PyutType
from org.pyut.model.PyutUseCase import PyutUseCase
from org.pyut.model.PyutStereotype import getPyutStereotype
from org.pyut.model.PyutModifier import PyutModifier
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.enums.LinkType import LinkType

from org.pyut.ogl.OglActor import OglActor
from org.pyut.ogl.OglAssociationLabel import OglAssociationLabel
from org.pyut.ogl.OglClass import OglClass

from org.pyut.ogl.OglInterface2 import OglInterface2
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglUseCase import OglUseCase
from org.pyut.ogl.OglAssociation import OglAssociation
from org.pyut.ogl.OglLinkFactory import getOglLinkFactory

from org.pyut.ogl.sd.OglSDInstance import OglSDInstance
from org.pyut.ogl.sd.OglSDMessage import OglSDMessage

from org.pyut.persistence.converters.PyutXmlConstants import PyutXmlConstants

from org.pyut.PyutUtils import PyutUtils

from org.pyut.ui.UmlFrame import UmlFrame

OglObjects     = NewType('OglObjects',     Dict[int, OglObject])
OglClasses     = NewType('OglClasses',     Dict[int, OglClass])
OglNotes       = NewType('OglNotes',       Dict[int, OglNote])
OglActors      = NewType('OglActors',      Dict[int, OglActor])
OglUseCases    = NewType('OglUseCases',    Dict[int, OglUseCase])
OglSDInstances = NewType('OglSDInstances', Dict[int, OglSDInstance])
OglSDMessages  = NewType('OglSDMessages',  Dict[int, OglSDMessage])
PyutMethods    = NewType('PyutMethods',    List[PyutMethod])
PyutFields     = NewType('PyutFields',     List[PyutField])
ControlPoints  = NewType('ControlPoints',  List[ControlPoint])
Links          = NewType('Links',          Union[OglLink, OglSDInstance])
OglLinks       = NewType('OglLinks',       List[Links])
OglInterfaces  = NewType('OglInterfaces',  List[OglInterface2])


class MiniDomToOgl:

    """
    The refactored version of the original methods that were part of the monolithic
     `PyutXml`xxx classes.  This version does NO UI related actions;  It is up to the
    caller to actually place the visual OGL object on the diagram frame

    """
    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def getOglClasses(self, xmlOglClasses: NodeList) -> OglClasses:
        """
        Loads to OGL objects
        Parse the XML elements given and build data model for the Pyut classes.

        Args:
            xmlOglClasses:   XML 'GraphicClass' elements

        Returns:
                The built dictionary uses an ID for the key and an OglClass for the value
        """
        oglObjects: OglClasses = cast(OglClasses, {})

        for xmlOglClass in xmlOglClasses:

            xmlOglClass: Element   = cast(Element, xmlOglClass)
            pyutClass:   PyutClass = PyutClass()

            height: float      = float(xmlOglClass.getAttribute(PyutXmlConstants.ATTR_HEIGHT))
            width:  float      = float(xmlOglClass.getAttribute(PyutXmlConstants.ATTR_WIDTH))

            oglClass: OglClass = OglClass(pyutClass, width, height)

            xmlClass: Element = xmlOglClass.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_CLASS)[0]

            pyutClass.setId(int(xmlClass.getAttribute(PyutXmlConstants.ATTR_ID)))
            pyutClass.setName(xmlClass.getAttribute(PyutXmlConstants.ATTR_NAME))
            pyutClass.description = xmlClass.getAttribute(PyutXmlConstants.ATTR_DESCRIPTION)
            if xmlClass.hasAttribute(PyutXmlConstants.ATTR_STEREOTYPE):
                pyutClass.setStereotype(getPyutStereotype(xmlClass.getAttribute(PyutXmlConstants.ATTR_STEREOTYPE)))

            # adding display properties (cd)
            value = PyutUtils.secureBoolean(xmlClass.getAttribute(PyutXmlConstants.ATTR_SHOW_STEREOTYPE))
            pyutClass.setShowStereotype(value)
            value = PyutUtils.secureBoolean(xmlClass.getAttribute(PyutXmlConstants.ATTR_SHOW_METHODS))
            pyutClass.showMethods = value
            value = PyutUtils.secureBoolean(xmlClass.getAttribute(PyutXmlConstants.ATTR_SHOW_FIELDS))
            pyutClass.showFields = value

            displayParametersStr: str = xmlOglClass.getAttribute(PyutXmlConstants.ATTR_DISPLAY_PARAMETERS)

            if displayParametersStr is None or displayParametersStr == '':
                pyutClass.displayParameters = PyutDisplayParameters.UNSPECIFIED
            else:
                displayParameters: PyutDisplayParameters = PyutDisplayParameters(displayParametersStr)
                pyutClass.displayParameters = displayParameters

            pyutClass.setFilename(xmlClass.getAttribute(PyutXmlConstants.ATTR_FILENAME))

            pyutClass.methods = self._getMethods(xmlClass)
            pyutClass.fields  = self._getFields(xmlClass)

            # Adding properties necessary to place shape on a diagram frame
            x = float(xmlOglClass.getAttribute(PyutXmlConstants.ATTR_X))
            y = float(xmlOglClass.getAttribute(PyutXmlConstants.ATTR_Y))

            oglClass.SetPosition(x, y)

            oglObjects[pyutClass.getId()] = oglClass

        return oglObjects

    def getOglInterfaces(self, xmlOglInterfaces: NodeList) -> OglInterfaces:

        oglInterfaces: OglInterfaces = cast(OglInterfaces, [])

        for xmlOglInterface in xmlOglInterfaces:

            anchorPoint: SelectAnchorPoint  = self.__getAttachmentPoint(xmlOglInterface)

            xmlInterface:  Element = xmlOglInterface.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_INTERFACE)[0]

            pyutInterface: PyutInterface = PyutInterface()
            pyutInterface.name         = xmlInterface.getAttribute(PyutXmlConstants.ATTR_NAME)
            pyutInterface.description  = xmlOglInterface.getAttribute(PyutXmlConstants.ATTR_DESCRIPTION)
            pyutInterface.methods      = self._getMethods(xmlInterface)
            pyutInterface.implementors = self._getImplementors(xmlInterface)

            oglInterface: OglInterface2 = OglInterface2(pyutInterface=pyutInterface, destinationAnchor=anchorPoint)

            oglInterfaces.append(oglInterface)

        return oglInterfaces

    def getOglLinks(self, xmlOglLinks: NodeList, oglClasses: OglObjects) -> OglLinks:
        """
        Extract the link for the OglClasses

        Args:
            xmlOglLinks:    A DOM node list of links
            oglClasses:  The OglClasses

        Returns:
            The OglLinks list
        """
        oglLinks: OglLinks = cast(OglLinks, [])

        for xmlLink in xmlOglLinks:
            # src and dst anchor position
            xmlLink: Element = cast(Element, xmlLink)

            sx = PyutUtils.secureFloat(xmlLink.getAttribute(PyutXmlConstants.ATTR_LINK_SOURCE_ANCHOR_X))
            sy = PyutUtils.secureFloat(xmlLink.getAttribute(PyutXmlConstants.ATTR_LINK_SOURCE_ANCHOR_Y))
            dx = PyutUtils.secureFloat(xmlLink.getAttribute(PyutXmlConstants.ATTR_LINK_DESTINATION_ANCHOR_X))
            dy = PyutUtils.secureFloat(xmlLink.getAttribute(PyutXmlConstants.ATTR_LINK_DESTINATION_ANCHOR_Y))

            spline: bool = PyutUtils.secureBoolean(xmlLink.getAttribute(PyutXmlConstants.ATTR_SPLINE))

            # get the associated PyutLink
            srcId, dstId, assocPyutLink = self._getPyutLink(xmlLink)

            try:
                src: OglClass = oglClasses[srcId]
                dst: OglClass = oglClasses[dstId]
            except KeyError as ke:
                self.logger.error(f'Developer Error -- srcId: {srcId} - dstId: {dstId}  error: {ke}')
                continue

            linkType: LinkType = assocPyutLink.getType()
            pyutLink: PyutLink = PyutLink(name=assocPyutLink.getName(),
                                          linkType=linkType,
                                          cardSrc=assocPyutLink.sourceCardinality,
                                          cardDest=assocPyutLink.destinationCardinality,
                                          source=src.getPyutObject(), destination=dst.getPyutObject())

            oglLinkFactory = getOglLinkFactory()
            oglLink = oglLinkFactory.getOglLink(src, pyutLink, dst, linkType)
            src.addLink(oglLink)
            dst.addLink(oglLink)

            oglLinks.append(oglLink)

            oglLink.SetSpline(spline)

            # put the anchors at the right position
            srcAnchor = oglLink.GetSource()
            dstAnchor = oglLink.GetDestination()
            srcAnchor.SetPosition(sx, sy)
            dstAnchor.SetPosition(dx, dy)

            # add the control points to the line
            line   = srcAnchor.GetLines()[0]  # only 1 line per anchor in pyut
            parent = line.GetSource().GetParent()
            selfLink = parent is line.GetDestination().GetParent()

            controlPoints: ControlPoints = self._generateControlPoints(xmlLink)
            for controlPoint in controlPoints:
                line.AddControl(controlPoint)
                if selfLink:
                    x, y = controlPoint.GetPosition()
                    controlPoint.SetParent(parent)
                    controlPoint.SetPosition(x, y)

            if isinstance(oglLink, OglAssociation):
                self.__furtherCustomizeAssociationLink(xmlLink, oglLink)
            self._reconstituteLinkDataModel(oglLink)

        return oglLinks

    def getOglNotes(self, xmlOglNotes: NodeList) -> OglNotes:
        """
        Parse the XML elements given and build data layer for PyUt notes.

        Args:
            xmlOglNotes:        XML 'GraphicNote' elements

        Returns:
            The returned dictionary uses a generated ID for the key
        """
        oglNotes: OglNotes = cast(OglNotes, {})
        for xmlOglNote in xmlOglNotes:

            pyutNote: PyutNote = PyutNote()

            # Building OGL Note
            height: float = float(xmlOglNote.getAttribute(PyutXmlConstants.ATTR_HEIGHT))
            width:  float = float(xmlOglNote.getAttribute(PyutXmlConstants.ATTR_WIDTH))
            oglNote = OglNote(pyutNote, width, height)

            xmlNote: Element = xmlOglNote.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_NOTE)[0]

            pyutNote.setId(int(xmlNote.getAttribute(PyutXmlConstants.ATTR_ID)))

            content: str = xmlNote.getAttribute(PyutXmlConstants.ATTR_CONTENT)
            content = content.replace("\\\\\\\\", "\n")

            pyutNote.content = content

            pyutNote.setFilename(xmlNote.getAttribute(PyutXmlConstants.ATTR_FILENAME))

            # Adding properties necessary to place shape on a diagram frame
            x: float = float(xmlOglNote.getAttribute(PyutXmlConstants.ATTR_X))
            y: float = float(xmlOglNote.getAttribute(PyutXmlConstants.ATTR_Y))

            oglNote.SetPosition(x, y)
            # Update the dictionary
            oglNotes[pyutNote.getId()] = oglNote

        return oglNotes

    def getOglActors(self, xmlOglActors: NodeList) -> OglActors:
        """
        Parse the XML elements given and build data layer for PyUt actors.

        Args:
            xmlOglActors:       XML 'GraphicActor' elements

        Returns:
            A dictionary of OglActor objects
        """
        oglActors: OglActors = cast(OglActors, {})

        for xmlOglActor in xmlOglActors:
            pyutActor: PyutActor = PyutActor()

            # Building OGL Actor
            height: float = float(xmlOglActor.getAttribute(PyutXmlConstants.ATTR_HEIGHT))
            width:  float = float(xmlOglActor.getAttribute(PyutXmlConstants.ATTR_WIDTH))
            oglActor: OglActor = OglActor(pyutActor, width, height)

            xmlActor: Element = xmlOglActor.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_ACTOR)[0]

            pyutActor.setId(int(xmlActor.getAttribute(PyutXmlConstants.ATTR_ID)))
            pyutActor.setName(xmlActor.getAttribute(PyutXmlConstants.ATTR_NAME))
            pyutActor.setFilename(xmlActor.getAttribute(PyutXmlConstants.ATTR_FILENAME))

            # Adding properties necessary to place shape on a diagram frame
            x = float(xmlOglActor.getAttribute(PyutXmlConstants.ATTR_X))
            y = float(xmlOglActor.getAttribute(PyutXmlConstants.ATTR_Y))
            oglActor.SetPosition(x, y)

            oglActors[pyutActor.getId()] = oglActor

        return oglActors

    def getOglUseCases(self, xmlOglUseCases: NodeList) -> OglUseCases:
        """
        Parse the XML elements given and build data layer for PyUt actors.

        Args:
            xmlOglUseCases:     XML 'GraphicUseCase' elements

        Returns:
            A dictionary of OglUseCase objects
        """
        oglUseCases: OglUseCases = cast(OglUseCases, {})

        for xmlOglUseCase in xmlOglUseCases:

            pyutUseCase: PyutUseCase = PyutUseCase()

            # Building OGL UseCase
            height = float(xmlOglUseCase.getAttribute(PyutXmlConstants.ATTR_HEIGHT))
            width = float(xmlOglUseCase.getAttribute(PyutXmlConstants.ATTR_WIDTH))
            oglUseCase = OglUseCase(pyutUseCase, width, height)

            xmlUseCase: Element = xmlOglUseCase.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_USE_CASE)[0]

            pyutUseCase.setId(int(xmlUseCase.getAttribute(PyutXmlConstants.ATTR_ID)))
            pyutUseCase.setName(xmlUseCase.getAttribute(PyutXmlConstants.ATTR_NAME))
            pyutUseCase.setFilename(xmlUseCase.getAttribute(PyutXmlConstants.ATTR_FILENAME))

            x = float(xmlOglUseCase.getAttribute(PyutXmlConstants.ATTR_X))
            y = float(xmlOglUseCase.getAttribute(PyutXmlConstants.ATTR_Y))
            oglUseCase.SetPosition(x, y)

            oglUseCases[pyutUseCase.getId()] = oglUseCase

        return oglUseCases

    def getOglSDInstances(self, xmlOglSDInstances: NodeList, umlFrame: UmlFrame) -> OglSDInstances:
        """
        Parse the given XML elements and build data layer for PyUT sequence diagram instances.

        Args:
            xmlOglSDInstances:
            umlFrame:  Because of the way SDInstances are constructed they need access
            to the diagram frame

        Returns:
            A dictionary of OglSDInstance objects
        """
        oglSDInstances: OglSDInstances = cast(OglSDInstances, {})
        for xmlOglSDInstance in xmlOglSDInstances:

            pyutSDInstance: PyutSDInstance = PyutSDInstance()
            oglSDInstance:  OglSDInstance  = OglSDInstance(pyutSDInstance, umlFrame)

            xmlSDInstance = xmlOglSDInstance.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_SD_INSTANCE)[0]

            pyutSDInstance.setId(int(xmlSDInstance.getAttribute(PyutXmlConstants.ATTR_ID)))
            pyutSDInstance.setInstanceName(xmlSDInstance.getAttribute(PyutXmlConstants.ATTR_INSTANCE_NAME))

            lifeLineLength: int = PyutUtils.secureInteger(xmlSDInstance.getAttribute(PyutXmlConstants.ATTR_LIFE_LINE_LENGTH))
            pyutSDInstance.setInstanceLifeLineLength(lifeLineLength)

            # Adding OGL class to UML Frame
            x = float(xmlOglSDInstance.getAttribute(PyutXmlConstants.ATTR_X))
            y = float(xmlOglSDInstance.getAttribute(PyutXmlConstants.ATTR_Y))
            w = float(xmlOglSDInstance.getAttribute(PyutXmlConstants.ATTR_WIDTH))
            h = float(xmlOglSDInstance.getAttribute(PyutXmlConstants.ATTR_HEIGHT))
            oglSDInstance.SetSize(w, h)
            oglSDInstance.SetPosition(x, y)

            oglSDInstances[pyutSDInstance.getId()] = oglSDInstance

            # umlFrame.addShape(oglSDInstance, x, y)        # currently SD Instance constructor adds itself

        return oglSDInstances

    def getOglSDMessages(self, xmlOglSDMessages: NodeList, oglSDInstances: OglSDInstances) -> OglSDMessages:
        """
        Parse the given XML elements and build data layer for PyUT sequence diagram messages.

        Args:
            xmlOglSDMessages:
            oglSDInstances:

        Returns:
            A dictionary of OglSDMessage objects
        """
        oglSDMessages: OglSDMessages = cast(OglSDMessages, {})

        for xmlOglSDMessage in xmlOglSDMessages:

            # Data layer class
            xmlPyutSDMessage: Element = xmlOglSDMessage.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_SD_MESSAGE)[0]

            # Building OGL
            pyutSDMessage: PyutSDMessage = PyutSDMessage()

            srcID: int = int(xmlPyutSDMessage.getAttribute(PyutXmlConstants.ATTR_SD_MESSAGE_SOURCE_ID))
            dstID: int = int(xmlPyutSDMessage.getAttribute(PyutXmlConstants.ATTR_SD_MESSAGE_DESTINATION_ID))
            srcTime: int = int(float(xmlPyutSDMessage.getAttribute(PyutXmlConstants.ATTR_SOURCE_TIME_LINE)))
            dstTime: int = int(float(xmlPyutSDMessage.getAttribute(PyutXmlConstants.ATTR_DESTINATION_TIME_LINE)))
            srcOgl = oglSDInstances[srcID]
            dstOgl = oglSDInstances[dstID]

            oglSDMessage: OglSDMessage = OglSDMessage(srcOgl, pyutSDMessage, dstOgl)
            pyutSDMessage.setOglObject(oglSDMessage)
            pyutSDMessage.setSource(srcOgl.getPyutObject(), srcTime)
            pyutSDMessage.setDestination(dstOgl.getPyutObject(), dstTime)

            # Pyut Data
            pyutSDMessage.setId(int(xmlPyutSDMessage.getAttribute(PyutXmlConstants.ATTR_ID)))
            pyutSDMessage.setMessage(xmlPyutSDMessage.getAttribute(PyutXmlConstants.ATTR_MESSAGE))

            oglSDMessages[pyutSDMessage.getId()] = oglSDMessage

            # Adding OGL class to UML Frame
            # diagram = umlFrame.GetDiagram()
            oglSDInstances[srcID].addLink(oglSDMessage)
            oglSDInstances[dstID].addLink(oglSDMessage)
            # diagram.AddShape(oglSDMessage)

        return oglSDMessages

    def _getMethods(self, xmlClass: Element) -> PyutMethods:
        """
        Converts XML methods to `PyutMethod`s
        Args:
            xmlClass:  A DOM element that is a UML Class

        Returns:
            A list of `PyutMethod`s associated with the class
        """
        allMethods: PyutMethods = cast(PyutMethods, [])
        for xmlMethod in xmlClass.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_METHOD):

            pyutMethod: PyutMethod = PyutMethod(xmlMethod.getAttribute(PyutXmlConstants.ATTR_NAME))

            strVis: str = xmlMethod.getAttribute(PyutXmlConstants.ATTR_VISIBILITY)
            vis: PyutVisibilityEnum = PyutVisibilityEnum.toEnum(strVis)
            pyutMethod.setVisibility(visibility=vis)

            returnElt:  Element  = xmlMethod.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_RETURN)[0]
            retTypeStr: str      = returnElt.getAttribute(PyutXmlConstants.ATTR_TYPE)
            retType:    PyutType = PyutType(retTypeStr)
            pyutMethod.setReturns(retType)

            #
            #  Code supports multiple modifiers, but the dialog allows input of only one
            #
            modifiers: NodeList = xmlMethod.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_MODIFIER)
            for xmlModifier in modifiers:
                xmlModifier: Element = cast(Element, xmlModifier)
                modName:  str        = xmlModifier.getAttribute(PyutXmlConstants.ATTR_NAME)

                pyutModifier: PyutModifier = PyutModifier(modName)
                pyutMethod.addModifier(pyutModifier)

            methodParameters = []
            for xmlParam in xmlMethod.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_PARAM):
                methodParameters.append(self._getParam(xmlParam))

            pyutMethod.setParams(methodParameters)

            allMethods.append(pyutMethod)

        return allMethods

    def _getImplementors(self, xmlClass: Element) -> PyutInterface.Implementors:

        implementors: PyutInterface.Implementors = []
        for xmlImplementor in xmlClass.getElementsByTagName(PyutXmlConstants.ELEMENT_IMPLEMENTOR):
            className: PyutInterface.ClassName = xmlImplementor.getAttribute(PyutXmlConstants.ATTR_IMPLEMENTING_CLASS_NAME)
            implementors.append(className)

        return implementors

    def _getParam(self, domElement: Element) -> PyutParam:
        """

        Args:
            domElement:  The xml element tht is a parameter

        Returns:
            A parameter model object
        """
        paramTypeStr: str = domElement.getAttribute(PyutXmlConstants.ATTR_TYPE)
        paramType:    PyutType = PyutType(paramTypeStr)
        pyutParam: PyutParam = PyutParam(name=domElement.getAttribute(PyutXmlConstants.ATTR_NAME),
                                         theParameterType=paramType)

        if domElement.hasAttribute(PyutXmlConstants.ATTR_DEFAULT_VALUE):
            pyutParam.setDefaultValue(domElement.getAttribute(PyutXmlConstants.ATTR_DEFAULT_VALUE))

        return pyutParam

    def _getFields(self, xmlClass: Element) -> PyutFields:
        """
        Extracts fields from a DOM element that represents a UML class

        Args:
            xmlClass:
                The DOM version of a UML class

        Returns:
            PyutFields
        """
        pyutFields: PyutFields = cast(PyutFields, [])

        for xmlField in xmlClass.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_FIELD):

            xmlField:   Element  = cast(Element, xmlField)
            pyutField: PyutField = PyutField()

            strVis: str                = xmlField.getAttribute(PyutXmlConstants.ATTR_VISIBILITY)
            vis:    PyutVisibilityEnum = PyutVisibilityEnum.toEnum(strVis)

            pyutField.setVisibility(vis)
            xmlParam: Element = xmlField.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_PARAM)[0]

            if xmlParam.hasAttribute(PyutXmlConstants.ATTR_DEFAULT_VALUE):
                pyutField.setDefaultValue(xmlParam.getAttribute(PyutXmlConstants.ATTR_DEFAULT_VALUE))
            pyutField.setName(xmlParam.getAttribute(PyutXmlConstants.ATTR_NAME))

            pyutType: PyutType = PyutType(xmlParam.getAttribute(PyutXmlConstants.ATTR_TYPE))
            pyutField.setType(pyutType)

            pyutFields.append(pyutField)

        return pyutFields

    def _generateControlPoints(self, link: Element) -> ControlPoints:

        controlPoints: ControlPoints = cast(ControlPoints, [])

        for controlPoint in link.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_CONTROL_POINT):
            x = PyutUtils.secureFloat(controlPoint.getAttribute(PyutXmlConstants.ATTR_X))
            y = PyutUtils.secureFloat(controlPoint.getAttribute(PyutXmlConstants.ATTR_Y))
            controlPoints.append(ControlPoint(x, y))

        return controlPoints

    def _reconstituteLinkDataModel(self, oglLink: OglLink):
        """
        Updates one the following lists in a PyutLinkedObject:

        ._parents   for Inheritance links
        ._links     for all other link types

        Args:
            oglLink:       An OglLink
        """
        srcShape:  OglClass = oglLink.getSourceShape()
        destShape: OglClass = oglLink.getDestinationShape()
        self.logger.debug(f'source ID: {srcShape.GetID()} - destination ID: {destShape.GetID()}')

        pyutLink:        PyutLink = oglLink.getPyutObject()

        if pyutLink.getType() == LinkType.INHERITANCE:
            childPyutClass:  PyutClass = srcShape.getPyutObject()
            parentPyutClass: PyutClass = destShape.getPyutObject()
            childPyutClass.addParent(parentPyutClass)
        else:
            srcPyutClass:  PyutClass = srcShape.getPyutObject()
            srcPyutClass.addLink(pyutLink)

    def _getPyutLink(self, obj: Element):
        """

        Args:
            obj:  The GraphicLink DOM element

        Returns:
            A tuple of a source ID, destination ID, and a PyutLink object
        """
        link: Element = obj.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_LINK)[0]

        pyutLink: PyutLink = PyutLink()

        pyutLink.setBidir(bool(link.getAttribute(PyutXmlConstants.ATTR_BIDIRECTIONAL)))

        pyutLink.destinationCardinality = link.getAttribute(PyutXmlConstants.ATTR_CARDINALITY_DESTINATION)
        pyutLink.sourceCardinality      = link.getAttribute(PyutXmlConstants.ATTR_CARDINALITY_SOURCE)

        pyutLink.setName(link.getAttribute(PyutXmlConstants.ATTR_NAME))

        strLinkType: str         = link.getAttribute(PyutXmlConstants.ATTR_TYPE)
        linkType:    LinkType    = LinkType.toEnum(strValue=strLinkType)
        pyutLink.setType(linkType)

        # source and destination will be reconstructed by _getOglLinks
        sourceId = int(link.getAttribute(PyutXmlConstants.ATTR_SOURCE_ID))
        destId   = int(link.getAttribute(PyutXmlConstants.ATTR_DESTINATION_ID))

        return sourceId, destId, pyutLink

    def __furtherCustomizeAssociationLink(self, xmlLink: Element, oglLink: OglAssociation):
        """
        Customize the visual aspects of an Association link
        Args:
            xmlLink:
            oglLink:
        """
        center: OglAssociationLabel = oglLink.centerLabel
        src:    OglAssociationLabel = oglLink.sourceCardinality
        dest:   OglAssociationLabel = oglLink.destinationCardinality

        self.__setAssociationLabelPosition(xmlLink, PyutXmlConstants.ELEMENT_ASSOC_CENTER_LABEL,      center)
        self.__setAssociationLabelPosition(xmlLink, PyutXmlConstants.ELEMENT_ASSOC_SOURCE_LABEL,      src)
        self.__setAssociationLabelPosition(xmlLink, PyutXmlConstants.ELEMENT_ASSOC_DESTINATION_LABEL, dest)

    def __setAssociationLabelPosition(self, xmlLink: Element, tagName: str, associationLabel: OglAssociationLabel):
        """

        Args:
            xmlLink:
            tagName:
            associationLabel:
        """
        label:  Element   = xmlLink.getElementsByTagName(tagName)[0]
        x = float(label.getAttribute(PyutXmlConstants.ATTR_X))
        y = float(label.getAttribute(PyutXmlConstants.ATTR_Y))

        self.logger.debug(f'tagName: {tagName} `{associationLabel.text=}`  pos: ({x:.2f},{y:.2f})')

        associationLabel.x = x
        associationLabel.y = y

    def __getAttachmentPoint(self, xmlOglInterface: Element) -> SelectAnchorPoint:

        attachmentPointStr: str = xmlOglInterface.getAttribute(PyutXmlConstants.ATTR_LOLLIPOP_ATTACHMENT_POINT)
        xStr:        str = xmlOglInterface.getAttribute(PyutXmlConstants.ATTR_X)
        yStr:        str = xmlOglInterface.getAttribute(PyutXmlConstants.ATTR_Y)

        x: float = PyutUtils.secureFloat(xStr)
        y: float = PyutUtils.secureFloat(yStr)

        attachmentPoint: AttachmentPoint   = AttachmentPoint.toEnum(attachmentPointStr)
        anchorPoint:     SelectAnchorPoint = SelectAnchorPoint(x=x, y=y, attachmentPoint=attachmentPoint)

        return anchorPoint
