
from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document
from xml.dom.minidom import Element

from org.pyut.PyutActor import PyutActor
from org.pyut.PyutClass import PyutClass
from org.pyut.PyutField import PyutField
from org.pyut.PyutNote import PyutNote
from org.pyut.PyutParam import PyutParam
from org.pyut.PyutVisibilityEnum import PyutVisibilityEnum
from org.pyut.ogl.OglActor import OglActor

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglObject import OglObject

from org.pyut.persistence.converters.PyutXmlConstants import PyutXmlConstants
from org.pyut.persistence.converters.IDFactorySingleton import IDFactory


class ToPyutXml:
    """
    The refactored version of the original methods that were part of the monolithic
     PyutXml`xxx` classes.

     This version is
        * renamed for clarity
        * uses typing for developer clarity
        * removes 'magic' strings shared between it and the ToOgl class
        * updated to use google docstrings

    """
    def __init__(self):

        self.logger:     Logger    = getLogger(__name__)
        self._idFactory: IDFactory = IDFactory()

    def oglClassToXml(self, oglClass: OglClass, xmlDoc: Document) -> Element:
        """
        Exports an OglClass to a minidom Element.

        Args:
            oglClass:   Graphic Class to save
            xmlDoc:     The document to append to

        Returns:
            The newly created `GraphicClass` element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_GRAPHIC_CLASS)

        root = self.__appendOglBase(oglClass, root)

        # adding the data layer object
        root.appendChild(self._pyutClassToXml(oglClass.getPyutObject(), xmlDoc))

        return root

    def oglNoteToXml(self, oglNote: OglNote, xmlDoc: Document) -> Element:
        """
        Export an OglNote to a minidom Element.

        Args:
            oglNote:    Note to convert
            xmlDoc:     xml document

        Returns:
            New minidom element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_GRAPHIC_NOTE)

        self.__appendOglBase(oglNote, root)

        root.appendChild(self._pyutNoteToXml(oglNote.getPyutObject(), xmlDoc))

        return root

    def oglActor2xml(self, oglActor: OglActor, xmlDoc: Document) -> Element:
        """
        Exporting an OglActor to a minidom Element.

        Args:
            oglActor:   Actor to convert
            xmlDoc:     xml document

        Returns:
            New minidom element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_GRAPHIC_ACTOR)

        self.__appendOglBase(oglActor, root)

        root.appendChild(self._pyutActorToXml(oglActor.getPyutObject(), xmlDoc))

        return root

    def __appendOglBase(self, oglObject: OglObject, root: Element) -> Element:
        """
        Saves the position and size of the OGL object in XML node.

        Args:
            oglObject:  OGL Object
            root:      XML node to update

        Returns:
            The updated element
        """
        # Saving size
        w, h = oglObject.GetModel().GetSize()
        root.setAttribute(PyutXmlConstants.ATTR_WIDTH,  str(float(w)))
        root.setAttribute(PyutXmlConstants.ATTR_HEIGHT, str(float(h)))

        # Saving position
        x, y = oglObject.GetModel().GetPosition()
        root.setAttribute(PyutXmlConstants.ATTR_X, str(x))
        root.setAttribute(PyutXmlConstants.ATTR_Y, str(y))

        return root

    def _pyutClassToXml(self, pyutClass: PyutClass, xmlDoc: Document) -> Element:
        """
        Exporting a PyutClass to a miniDom Element.

        Args:
            pyutClass:  The pyut class to save
            xmlDoc:     The xml document to update

        Returns:
            The new updated element
        """
        root = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_CLASS)

        classId: int = self._idFactory.getID(pyutClass)
        root.setAttribute(PyutXmlConstants.ATTR_ID, str(classId))
        root.setAttribute(PyutXmlConstants.ATTR_NAME, pyutClass.getName())

        stereotype = pyutClass.getStereotype()
        if stereotype is not None:
            root.setAttribute(PyutXmlConstants.ATTR_STEREOTYPE, stereotype.getStereotype())

        root.setAttribute(PyutXmlConstants.ATTR_DESCRIPTION, pyutClass.getDescription())
        root.setAttribute(PyutXmlConstants.ATTR_FILENAME,    pyutClass.getFilename())
        root.setAttribute(PyutXmlConstants.ATTR_SHOW_METHODS, str(pyutClass.getShowMethods()))
        root.setAttribute(PyutXmlConstants.ATTR_SHOW_FIELDS,  str(pyutClass.getShowFields()))
        root.setAttribute(PyutXmlConstants.ATTR_SHOW_STEREOTYPE,   str(pyutClass.getShowStereotype()))
        # methods
        for method in pyutClass.getMethods():
            root.appendChild(self._pyutMethodToXml(method, xmlDoc))
        # fields
        for field in pyutClass.getFields():
            root.appendChild(self._pyutFieldToXml(field, xmlDoc))

        return root

    def _pyutMethodToXml(self, pyutMethod, xmlDoc) -> Element:
        """
        Exporting a PyutMethod to a miniDom Element

        Args:
            pyutMethod: Method to save
            xmlDoc:     xml document

        Returns:
            The new updated element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_METHOD)

        root.setAttribute(PyutXmlConstants.ATTR_NAME, pyutMethod.getName())

        visibility: PyutVisibilityEnum = pyutMethod.getVisibility()
        visStr: str = visibility.__str__()
        if visibility is not None:
            root.setAttribute(PyutXmlConstants.ATTR_VISIBILITY, visStr)

        for modifier in pyutMethod.getModifiers():
            xmlModifier: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODIFIER)
            xmlModifier.setAttribute(PyutXmlConstants.ATTR_NAME, modifier.getName())
            root.appendChild(xmlModifier)

        returnType = pyutMethod.getReturns()
        if returnType is not None:
            xmlReturnType: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_RETURN)
            xmlReturnType.setAttribute(PyutXmlConstants.ATTR_TYPE, str(returnType))
            root.appendChild(xmlReturnType)

        for param in pyutMethod.getParams():
            root.appendChild(self._pyutParamToXml(param, xmlDoc))

        return root

    def _pyutFieldToXml(self, pyutField: PyutField, xmlDoc: Document) -> Element:
        """
        Export a PyutField to a miniDom Element
        Args:
            pyutField:  The PyutField to save
            xmlDoc:     The xml document to update

        Returns:
            The new updated element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_FIELD)

        root.appendChild(self._pyutParamToXml(pyutField, xmlDoc))
        root.setAttribute(PyutXmlConstants.ATTR_VISIBILITY, str(pyutField.getVisibility()))

        return root

    def _pyutParamToXml(self, pyutParam: PyutParam, xmlDoc: Document) -> Element:
        """
        Export a PyutParam to a miniDom Element

        Args:
            pyutParam:  Parameter to save
            xmlDoc:     XML Node

        Returns:
            The new updated element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_PARAM)

        root.setAttribute(PyutXmlConstants.ATTR_NAME, pyutParam.getName())
        root.setAttribute(PyutXmlConstants.ATTR_TYPE, str(pyutParam.getType()))

        defaultValue = pyutParam.getDefaultValue()
        if defaultValue is not None:
            root.setAttribute(PyutXmlConstants.ATTR_DEFAULT_VALUE, defaultValue)

        return root

    def _pyutNoteToXml(self, pyutNote: PyutNote, xmlDoc: Document) -> Element:
        """
        Export a PyutNote to a miniDom Element.

        Args:
            pyutNote:   Note to convert
            xmlDoc:     xml document

        Returns:
            New miniDom element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_NOTE)

        noteId: int = self._idFactory.getID(pyutNote)
        root.setAttribute(PyutXmlConstants.ATTR_ID, str(noteId))

        name: str = pyutNote.getName()
        name = name.replace('\n', "\\\\\\\\")
        root.setAttribute(PyutXmlConstants.ATTR_NAME, name)
        root.setAttribute(PyutXmlConstants.ATTR_FILENAME, pyutNote.getFilename())

        return root

    def _pyutActorToXml(self, pyutActor: PyutActor, xmlDoc: Document) -> Element:
        """
        Export an PyutActor to a minidom Element.
        Args:
            pyutActor:  Actor to convert
            xmlDoc:     xml document

        Returns:
            A new minidom element
        """
        root: Element = xmlDoc.createElement(PyutXmlConstants.ELEMENT_MODEL_ACTOR)

        actorId = self._idFactory.getID(pyutActor)
        root.setAttribute(PyutXmlConstants.ATTR_ID, str(actorId))
        root.setAttribute(PyutXmlConstants.ATTR_NAME, pyutActor.getName())
        root.setAttribute(PyutXmlConstants.ATTR_FILENAME, pyutActor.getFilename())

        return root
