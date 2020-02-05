
from typing import cast
from typing import Dict
from typing import List
from typing import NewType

from logging import Logger
from logging import getLogger
from xml.dom.minidom import Element

from xml.dom.minidom import NodeList

from org.pyut.PyutClass import PyutClass
from org.pyut.PyutMethod import PyutMethod
from org.pyut.PyutParam import PyutParam
from org.pyut.PyutUtils import PyutUtils
from org.pyut.PyutVisibilityEnum import PyutVisibilityEnum
from org.pyut.ogl.OglClass import OglClass

from org.pyut.PyutStereotype import getPyutStereotype

OglClasses  = NewType('OglClasses',  Dict[int, OglClass])
PyutMethods = NewType('PyutMethods', List[PyutMethod])


class ToOgl:
    """
    The refactored version of this does NO UI related actions;  It is up to the
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
        dicoOglObjects: OglClasses = cast(OglClasses, {})

        for xmlOglClass in xmlOglClasses:

            xmlOglClass: Element   = cast(Element, xmlOglClass)
            pyutClass:   PyutClass = PyutClass()

            height: float      = float(xmlOglClass.getAttribute('height'))
            width:  float      = float(xmlOglClass.getAttribute('width'))
            oglClass: OglClass = OglClass(pyutClass, width, height)

            xmlClass: Element = xmlOglClass.getElementsByTagName('Class')[0]

            pyutClass.setId(int(xmlClass.getAttribute('id')))
            pyutClass.setName(xmlClass.getAttribute('name'))
            pyutClass.setDescription(xmlClass.getAttribute('description'))
            if xmlClass.hasAttribute('stereotype'):
                pyutClass.setStereotype(getPyutStereotype(xmlClass.getAttribute('stereotype')))

            # adding display properties (cd)
            value = PyutUtils.secureBoolean(xmlClass.getAttribute('showStereotype'))
            pyutClass.setShowStereotype(value)
            value = PyutUtils.secureBoolean(xmlClass.getAttribute('showMethods'))
            pyutClass.setShowMethods(value)
            value = PyutUtils.secureBoolean(xmlClass.getAttribute('showFields'))
            pyutClass.setShowFields(value)

            pyutClass.setFilename(xmlClass.getAttribute('filename'))

            # adding methods for this class
            pyutClass.setMethods(self._getMethods(xmlClass))

            # adding fields for this class
            #    TEMP pyutClass.setFields(self._getFields(xmlClass))

            dicoOglObjects[pyutClass.getId()] = oglClass

            # Adding properties necessary to place shape on diagram frame
            x = float(xmlOglClass.getAttribute('x'))
            y = float(xmlOglClass.getAttribute('y'))

            oglClass.SetPosition(x, y)

        return dicoOglObjects

    def _getMethods(self, xmlClass: Element) -> PyutMethods:
        """
        Converts XML methods to `PyutMethod`s
        Args:
            xmlClass:  A DOM element that is a UML Class

        Returns:
            A list of `PyutMethod`s associated with the class
        """
        allMethods: PyutMethods = cast(PyutMethods, [])
        for xmlMethod in xmlClass.getElementsByTagName("Method"):

            pyutMethod: PyutMethod = PyutMethod(xmlMethod.getAttribute('name'))

            strVis: str = xmlMethod.getAttribute('visibility')
            vis: PyutVisibilityEnum = PyutVisibilityEnum(strVis)
            pyutMethod.setVisibility(visibility=vis)

            returnElt: Element = xmlMethod.getElementsByTagName("Return")[0]
            pyutMethod.setReturns(returnElt.getAttribute('type'))

            methodParameters = []
            for xmlParam in xmlMethod.getElementsByTagName("Param"):
                methodParameters.append(self._getParam(xmlParam))

            pyutMethod.setParams(methodParameters)

            allMethods.append(pyutMethod)

        return allMethods

    def _getParam(self, domElement: Element) -> PyutParam:
        """

        Args:
            domElement:  The xml element tht is a paremeter

        Returns:
            A parameter model object
        """
        pyutParam: PyutParam = PyutParam(name=domElement.getAttribute('name'), theParameterType=domElement.getAttribute('type'))

        if domElement.hasAttribute('defaultValue'):
            pyutParam.setDefaultValue(domElement.getAttribute('defaultValue'))

        return pyutParam

