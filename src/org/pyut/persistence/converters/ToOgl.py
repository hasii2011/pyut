
from typing import cast
from typing import Dict
from typing import List
from typing import Union
from typing import NewType

from logging import Logger
from logging import getLogger

from xml.dom.minidom import Element
from xml.dom.minidom import NodeList

from org.pyut.MiniOgl.ControlPoint import ControlPoint
from org.pyut.MiniOgl.TextShape import TextShape
from org.pyut.PyutActor import PyutActor

from org.pyut.PyutClass import PyutClass
from org.pyut.PyutField import PyutField
from org.pyut.PyutLink import PyutLink
from org.pyut.PyutMethod import PyutMethod
from org.pyut.PyutNote import PyutNote
from org.pyut.PyutParam import PyutParam
from org.pyut.PyutSDInstance import PyutSDInstance
from org.pyut.PyutSDMessage import PyutSDMessage
from org.pyut.PyutUseCase import PyutUseCase
from org.pyut.PyutUtils import PyutUtils
from org.pyut.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.enums.OglLinkType import OglLinkType

from org.pyut.ogl.OglActor import OglActor
from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglLink import OglLink
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglUseCase import OglUseCase

from org.pyut.ogl.OglAssociation import OglAssociation
from org.pyut.ogl.OglAssociation import CENTER
from org.pyut.ogl.OglAssociation import DEST_CARD
from org.pyut.ogl.OglAssociation import SRC_CARD

from org.pyut.ogl.sd.OglSDInstance import OglSDInstance

from org.pyut.PyutStereotype import getPyutStereotype
from org.pyut.ogl.OglLinkFactory import getOglLinkFactory
from org.pyut.ogl.sd.OglSDMessage import OglSDMessage
from org.pyut.persistence.converters.PyutXmlConstants import PyutXmlConstants

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


class ToOgl:
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
            pyutClass.setDescription(xmlClass.getAttribute(PyutXmlConstants.ATTR_DESCRIPTION))
            if xmlClass.hasAttribute(PyutXmlConstants.ATTR_STEREOTYPE):
                pyutClass.setStereotype(getPyutStereotype(xmlClass.getAttribute(PyutXmlConstants.ATTR_STEREOTYPE)))

            # adding display properties (cd)
            value = PyutUtils.secureBoolean(xmlClass.getAttribute(PyutXmlConstants.ATTR_SHOW_STEREOTYPE))
            pyutClass.setShowStereotype(value)
            value = PyutUtils.secureBoolean(xmlClass.getAttribute(PyutXmlConstants.ATTR_SHOW_METHODS))
            pyutClass.setShowMethods(value)
            value = PyutUtils.secureBoolean(xmlClass.getAttribute(PyutXmlConstants.ATTR_SHOW_FIELDS))
            pyutClass.setShowFields(value)

            pyutClass.setFilename(xmlClass.getAttribute(PyutXmlConstants.ATTR_FILENAME))

            pyutClass.setMethods(self._getMethods(xmlClass))
            pyutClass.setFields(self._getFields(xmlClass))

            # Adding properties necessary to place shape on a diagram frame
            x = float(xmlOglClass.getAttribute(PyutXmlConstants.ATTR_X))
            y = float(xmlOglClass.getAttribute(PyutXmlConstants.ATTR_Y))

            oglClass.SetPosition(x, y)

            oglObjects[pyutClass.getId()] = oglClass

        return oglObjects

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

            linkType: OglLinkType = assocPyutLink.getType()
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
            line = srcAnchor.GetLines()[0]  # only 1 line per anchor in pyut
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

            name = xmlNote.getAttribute(PyutXmlConstants.ATTR_NAME)
            name = name.replace("\\\\\\\\", "\n")

            pyutNote.setName(name)

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

            xmlSDInstance = xmlOglSDInstance.getElementsByTagName('SDInstance')[0]

            pyutSDInstance.setId(int(xmlSDInstance.getAttribute(PyutXmlConstants.ATTR_ID)))
            pyutSDInstance.setInstanceName(xmlSDInstance.getAttribute('instanceName'))
            pyutSDInstance.setInstanceLifeLineLength(PyutUtils.secureInteger(xmlSDInstance.getAttribute('lifeLineLength')))

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
            xmlPyutSDMessage: Element = xmlOglSDMessage.getElementsByTagName('SDMessage')[0]

            # Building OGL
            pyutSDMessage: PyutSDMessage = PyutSDMessage()

            srcID: int = int(xmlPyutSDMessage.getAttribute('srcID'))
            dstID: int = int(xmlPyutSDMessage.getAttribute('dstID'))
            srcTime: int = int(float(xmlPyutSDMessage.getAttribute('srcTime')))
            dstTime: int = int(float(xmlPyutSDMessage.getAttribute('dstTime')))
            srcOgl = oglSDInstances[srcID]
            dstOgl = oglSDInstances[dstID]

            oglSDMessage: OglSDMessage = OglSDMessage(srcOgl, pyutSDMessage, dstOgl)
            pyutSDMessage.setOglObject(oglSDMessage)
            pyutSDMessage.setSource(srcOgl.getPyutObject(), srcTime)
            pyutSDMessage.setDestination(dstOgl.getPyutObject(), dstTime)

            # Pyut Data
            pyutSDMessage.setId(int(xmlPyutSDMessage.getAttribute(PyutXmlConstants.ATTR_ID)))
            pyutSDMessage.setMessage(xmlPyutSDMessage.getAttribute('message'))

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
            vis: PyutVisibilityEnum = PyutVisibilityEnum(strVis)
            pyutMethod.setVisibility(visibility=vis)

            returnElt: Element = xmlMethod.getElementsByTagName(PyutXmlConstants.ELEMENT_RETURN)[0]
            pyutMethod.setReturns(returnElt.getAttribute(PyutXmlConstants.ATTR_TYPE))

            methodParameters = []
            for xmlParam in xmlMethod.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_PARAM):
                methodParameters.append(self._getParam(xmlParam))

            pyutMethod.setParams(methodParameters)

            allMethods.append(pyutMethod)

        return allMethods

    def _getParam(self, domElement: Element) -> PyutParam:
        """

        Args:
            domElement:  The xml element tht is a parameter

        Returns:
            A parameter model object
        """
        pyutParam: PyutParam = PyutParam(name=domElement.getAttribute(PyutXmlConstants.ATTR_NAME),
                                         theParameterType=domElement.getAttribute(PyutXmlConstants.ATTR_TYPE))

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

            pyutField.setVisibility(xmlField.getAttribute(PyutXmlConstants.ATTR_VISIBILITY))
            xmlParam: Element = xmlField.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_PARAM)[0]

            if xmlParam.hasAttribute(PyutXmlConstants.ATTR_DEFAULT_VALUE):
                pyutField.setDefaultValue(xmlParam.getAttribute(PyutXmlConstants.ATTR_DEFAULT_VALUE))
            pyutField.setName(xmlParam.getAttribute(PyutXmlConstants.ATTR_NAME))
            pyutField.setType(xmlParam.getAttribute(PyutXmlConstants.ATTR_TYPE))

            pyutFields.append(pyutField)

        return pyutFields

    def _generateControlPoints(self, link: Element) -> ControlPoints:

        controlPoints: ControlPoints = cast(ControlPoints, [])

        for controlPoint in link.getElementsByTagName(PyutXmlConstants.ELEMENT_MODEL_CONTROL_POINT):
            x = PyutUtils.secureFloat(controlPoint.getAttribute(PyutXmlConstants.ATTR_X))
            y = PyutUtils.secureFloat(controlPoint.getAttribute(PyutXmlConstants.ATTR_Y))
            controlPoints.append(ControlPoint(x, y))

        return controlPoints

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
        linkType:    OglLinkType = OglLinkType[strLinkType]
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
        center: TextShape = oglLink.getLabels()[CENTER]
        src:    TextShape = oglLink.getLabels()[SRC_CARD]
        dst:    TextShape = oglLink.getLabels()[DEST_CARD]

        self.__setAssociationLabelPosition(xmlLink, PyutXmlConstants.ELEMENT_ASSOC_CENTER_LABEL,      center)
        self.__setAssociationLabelPosition(xmlLink, PyutXmlConstants.ELEMENT_ASSOC_SOURCE_LABEL,      src)
        self.__setAssociationLabelPosition(xmlLink, PyutXmlConstants.ELEMENT_ASSOC_DESTINATION_LABEL, dst)

    def __setAssociationLabelPosition(self, xmlLink: Element, tagName: str, textShape: TextShape):
        """

        Args:
            xmlLink:
            tagName:
            textShape:
        """
        label:  Element   = xmlLink.getElementsByTagName(tagName)[0]
        x = float(label.getAttribute(PyutXmlConstants.ATTR_X))
        y = float(label.getAttribute(PyutXmlConstants.ATTR_Y))

        self.logger.debug(f'tagName: {tagName} textShape.text: `{textShape.GetText()}`  pos: ({x:.2f},{y:.2f})')

        textShape.SetPosition(x, y)
