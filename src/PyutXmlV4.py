#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.7 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2002-1-9"

from PyutClass       import *
from PyutParam       import *
from PyutMethod      import *
from PyutField       import *
from PyutStereotype  import *
from PyutType        import *
from PyutConsts      import *

# reading file
from StringIO import StringIO
from UmlFrame import *
from OglClass import OglClass
from OglLink  import *
from OglAssociation import *
#import lang
import PyutXmlV3

def secure_int(x):
    if x is None:
        return 0
    elif x=="_DeprecatedNonBool: False":
        return 0
    elif x=="_DeprecatedNonBool: True":
        return 1
    else:
        return int(x)

class PyutXml(PyutXmlV3.PyutXml):
    """
    Class for saving and loading a PyUT UML diagram in XML.
    This class offers two main methods that are save() and load().
    Using the dom XML model, you can, with the saving method, get the
    diagram corresponding XML view. For loading, you have to parse
    the file and indicate the UML frame on which you want to draw
    (See `UmlFrame`).

    Sample use::

        # Write
        pyutXml = PyutXml()
        text = pyutXml.save(oglObjects)
        file.write(text)

        # Read
        dom = parse(StringIO(file.read()))
        pyutXml = PyutXml()
        myXml.open(dom, umlFrame)

    :version: $Revision: 1.7 $
    :author: Philippe Waelti
    :contact: pwaelti@eivd.ch
    """

    #>------------------------------------------------------------------------
    def __init__(self):
        """
        Constructor
        @author C.Dutoit
        """
        self._this_version = 4


#>------------------------------------------------------------------------
    #    Here begin saving file
#>------------------------------------------------------------------------



    def _PyutClass2xml(self, pyutClass, xmlDoc):
        """
        Exporting an PyutClass to an miniDom Element.

        @param PyutMethod pyutClass : Class to save
        @param xmlDoc : xml document
        @return Element : XML Node
        @author Deve Roux <droux@eivd.ch>
        @modified C.Dutoit/20021121 added display properties
        """
        root = xmlDoc.createElement('Class')

        # ID
        root.setAttribute('id', str(pyutClass.getId()))

        # class name
        root.setAttribute('name', pyutClass.getName())

        # classs stereotype
        stereotype = pyutClass.getStereotype()
        if stereotype is not None:
            root.setAttribute('stereotype', stereotype.getStereotype())

        # description (pwaelti@eivd.ch)
        root.setAttribute('description', pyutClass.getDescription())

        # filename (lb@alawa.ch)
        root.setAttribute('filename', pyutClass.getFilename())

        # display properties (cd)
        root.setAttribute('showMethods', str(pyutClass.getShowMethods()))
        root.setAttribute('showFields',  str(pyutClass.getShowFields()))
        root.setAttribute('showStereotype', str(pyutClass.getShowStereotype()))



        # methods
        for method in pyutClass.getMethods():
            root.appendChild(self._PyutMethod2xml(method, xmlDoc))

        # fields
        for field in pyutClass.getFields():
            root.appendChild(self._PyutField2xml(field, xmlDoc))

        return root




#>------------------------------------------------------------------------
    #   Here begins reading file
#>------------------------------------------------------------------------



    #>--------------------------------------------------------------------

    def _getOglClasses(self, xmlOglClasses, dicoOglObjects, dicoLink, \
            dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT classes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglClasses : XML 'GraphicClass' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} fathers: Inheritance
        @param UmlFrame umlFrame : Where to draw
        @author Philippe Waelti <pwaelti@eivd.ch>
        @modified C.Dutoit/20021121 added display properties
        """
        for xmlOglClass in xmlOglClasses:

            pyutClass = PyutClass()
            # Building OGL class
            height = float(xmlOglClass.getAttribute('height'))
            width = float(xmlOglClass.getAttribute('width'))
            oglClass = OglClass(pyutClass, width, height)

            # Data layer class
            xmlClass = xmlOglClass.getElementsByTagName('Class')[0]

            pyutClass.setId(int(xmlClass.getAttribute('id')))

            # adding name for this class
            pyutClass.setName(xmlClass.getAttribute('name').encode("charmap"))

            # adding description
            pyutClass.setDescription(xmlClass.getAttribute('description'))

            # adding stereotype
            if xmlClass.hasAttribute('stereotype'):
                pyutClass.setStereotype(
                    getPyutStereotype(xmlClass.getAttribute('stereotype')))

            # adding display properties (cd)
            value = secure_int(xmlClass.getAttribute('showStereotype'))
            pyutClass.setShowStereotype(value)
            value = secure_int(xmlClass.getAttribute('showMethods'))
            pyutClass.setShowMethods(value)
            value = secure_int(xmlClass.getAttribute('showFields'))
            pyutClass.setShowFields(value)

            # adding associated filename (lb@alawa.ch)
            pyutClass.setFilename(xmlClass.getAttribute('filename'))

            # adding methods for this class
            pyutClass.setMethods(self._getMethods(xmlClass))

            # adding fields for this class
            pyutClass.setFields(self._getFields(xmlClass))

            dicoOglObjects[pyutClass.getId()] = oglClass

            # Adding OGL class to UML Frame
            x = float(xmlOglClass.getAttribute('x'))
            y = float(xmlOglClass.getAttribute('y'))
            umlFrame.addShape(oglClass, x, y)
