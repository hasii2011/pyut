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
import wx

THIS_VERSION = 2

class PyutXml:
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
    #    Here begin saving file
#>------------------------------------------------------------------------

    def _PyutLink2xml(self, pyutLink, xmlDoc):
        """
        Exporting an PyutLink to a miniDom Element.

        @param PyutLink pyutLink : Link to save
        @param xmlDoc : xml document
        @return Element : XML Node
        @since 2.0
        @author Deve Roux <droux@eivd.ch>
        """

        root = xmlDoc.createElement('Link')
        # link name
        root.setAttribute('name', pyutLink.getName() )

        # link type
        root.setAttribute('type', str(pyutLink.getType()))

        # link cardinality source
        root.setAttribute('cardSrc', pyutLink.getSrcCard())

        # link cardinality destination
        root.setAttribute('cardDestination', pyutLink.getDestCard())

        # link bidir
        root.setAttribute('bidir', str(pyutLink.getBidir()))

        # link source
        root.setAttribute('sourceId', str(pyutLink.getSource().getId()))

        # link destination
        root.setAttribute('destId', str(pyutLink.getDestination().getId()))

        return root


#>------------------------------------------------------------------------

    def _PyutParam2xml(self, pyutParam, xmlDoc):
        """
        Exporting a PyutParam to an miniDom Element.

        @param PyutParam pyutParam : Parameters to save
        @param xmlDoc : xml document
        @return Element : XML Node
        @author Deve Roux <droux@eivd.ch>
        """
        root = xmlDoc.createElement('Param')

        # param name
        root.setAttribute('name', pyutParam.getName())

        # param type
        root.setAttribute('type', str(pyutParam.getType()))

        # param defaulf value
        defaultValue = pyutParam.getDefaultValue()
        if (defaultValue is not None):
            root.setAttribute('defaultValue', defaultValue)

        return root

    
#>------------------------------------------------------------------------

    def _PyutField2xml(self, pyutField, xmlDoc):
        """
        Exporting a PyutField to an miniDom Element

        @param PyutField pyutField : Field to save
        @param xmlDoc : xml document
        @return Element : XML Node
        @author Deve Roux <droux@eivd.ch>
        """
        root = xmlDoc.createElement('Field')

        # adding the parent XML
        # pyutField is a param
        root.appendChild(self._PyutParam2xml(pyutField, xmlDoc))

        # field visibility
        root.setAttribute('visibility', str(pyutField.getVisibility()))

        return root

#>------------------------------------------------------------------------

    def _PyutMethod2xml(self, pyutMethod, xmlDoc):
        """
        Exporting an PyutMethod to an miniDom Element.

        @param PyutMethod pyutMethod : Method to save
        @param xmlDoc : xml document
        @return Element : XML Node
        @author Deve Roux <droux@eivd.ch>
        """
        root = xmlDoc.createElement('Method')

        # method name
        root.setAttribute('name', pyutMethod.getName() )

        # method visibility
        visibility = pyutMethod.getVisibility()
        if visibility is not None:
            root.setAttribute('visibility', str(visibility.getVisibility()))

        # for all modifiers
        for modifier in pyutMethod.getModifiers():
            xmlModifier = xmlDoc.createElement('Modifier')
            xmlModifier.setAttribute('name', modifier.getName())
            root.appendChild(xmlModifier)

        # method return type
        returnType = pyutMethod.getReturns()
        if returnType is not None:
            xmlReturnType = xmlDoc.createElement('Return')
            xmlReturnType.setAttribute('type', str(returnType))
            root.appendChild(xmlReturnType)

        # method params
        for param in pyutMethod.getParams() :
            root.appendChild(self._PyutParam2xml(param, xmlDoc))

        return root

#>------------------------------------------------------------------------

    def _PyutClass2xml(self, pyutClass, xmlDoc):
        """
        Exporting an PyutClass to an miniDom Element.

        @param PyutMethod pyutClass : Class to save
        @param xmlDoc : xml document
        @return Element : XML Node
        @author Deve Roux <droux@eivd.ch>
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

        # methods
        for method in pyutClass.getMethods():
            root.appendChild(self._PyutMethod2xml(method, xmlDoc))

        # fields
        for field in pyutClass.getFields():
            root.appendChild(self._PyutField2xml(field, xmlDoc))

        return root

#>------------------------------------------------------------------------

    def _PyutNote2xml(self, pyutNote, xmlDoc):
        """
        Exporting an PyutNote to an miniDom Element.

        @param PyutNote pyutNote : Note to convert
        @param xmlDoc : xml document
        @return Element          : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        root = xmlDoc.createElement('Note')

        # ID
        root.setAttribute('id', str(pyutNote.getId()))

        # Note
        root.setAttribute('name', pyutNote.getName())

        return root

#>------------------------------------------------------------------------

    def _PyutActor2xml(self, pyutActor, xmlDoc):
        """
        Exporting an PyutActor to an miniDom Element.

        @param PyutNote pyutActor : Note to convert
        @param xmlDoc : xml document
        @return Element : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        root = xmlDoc.createElement('Actor')

        # ID
        root.setAttribute('id', str(pyutActor.getId()))

        # Note
        root.setAttribute('name', pyutActor.getName())

        return root

#>------------------------------------------------------------------------

    def _PyutUseCase2xml(self, pyutUseCase, xmlDoc):
        """
        Exporting an PyutUseCase to an miniDom Element.

        @param PyutNote pyutUseCase : Note to convert
        @param xmlDoc : xml document
        @return Element : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        root = xmlDoc.createElement('UseCase')

        # ID
        root.setAttribute('id', str(pyutUseCase.getId()))

        # Note
        root.setAttribute('name', pyutUseCase.getName())

        return root

#>------------------------------------------------------------------------

    def _appendOglBase(self, oglObject, root):
        """
        Saves the position and size of the OGL object in XML node.

        @param OglObject oglObject : OGL Object
        @param Element root : XML node to write
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        # Saving size
        w, h = oglObject.GetSize()
        root.setAttribute('width', str(float(w)))
        root.setAttribute('height', str(float(h)))

        # Saving position
        x, y = oglObject.GetPosition()
        root.setAttribute('x', str(x))
        root.setAttribute('y', str(y))

#>------------------------------------------------------------------------

    def _OglLink2xml(self, oglLink, xmlDoc):
        """
        @param xmlDoc : xml document
        """
        root = xmlDoc.createElement('GraphicLink')

        # Append OGL object base
        # save src and dst anchor points
        x, y = oglLink.GetSource().GetPosition()
        root.setAttribute('srcX', str(x))
        root.setAttribute('srcY', str(y))

        x, y = oglLink.GetDestination().GetPosition()
        root.setAttribute('dstX', str(x))
        root.setAttribute('dstY', str(y))

        root.setAttribute('spline', str(oglLink.GetSpline()))

        if isinstance(oglLink, OglAssociation):
            center = oglLink.getLabels()[CENTER]
            src = oglLink.getLabels()[SRC_CARD]
            dst = oglLink.getLabels()[DEST_CARD]
            label = xmlDoc.createElement("LabelCenter")
            root.appendChild(label)
            x, y = center.GetPosition()
            label.setAttribute("x", str(x))
            label.setAttribute("y", str(y))
            label = xmlDoc.createElement("LabelSrc")
            root.appendChild(label)
            x, y = src.GetPosition()
            label.setAttribute("x", str(x))
            label.setAttribute("y", str(y))
            label = xmlDoc.createElement("LabelDst")
            root.appendChild(label)
            x, y = dst.GetPosition()
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

#>------------------------------------------------------------------------

    def _OglClass2xml(self, oglClass, xmlDoc):
        """
        Exporting an OglClass to an miniDom Element.

        @param PyutMethod oglClass : Class to save
        @param xmlDoc : xml document
        @return Element : XML Node
        @author Deve Roux <droux@eivd.ch>
        """
        root = xmlDoc.createElement('GraphicClass')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglClass, root)

        # adding the data layer object
        root.appendChild(self._PyutClass2xml(oglClass.getPyutObject(), xmlDoc))

        return root

#>------------------------------------------------------------------------

    def _OglNote2xml(self, oglNote, xmlDoc):
        """
        Exporting an OglNote to an miniDom Element.

        @param OglNote oglNote : Note to convert
        @param xmlDoc : xml document
        @return Element        : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        root = xmlDoc.createElement('GraphicNote')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglNote, root)

        # adding the data layer object
        root.appendChild(self._PyutNote2xml(oglNote.getPyutObject(), xmlDoc))

        return root

    
#>------------------------------------------------------------------------

    def _OglActor2xml(self, oglActor, xmlDoc):
        """
        Exporting an OglActor to an miniDom Element.

        @param OglActor oglActor : Actor to convert
        @param xmlDoc : xml document
        @return Element : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        root = xmlDoc.createElement('GraphicActor')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglActor, root)

        # adding the data layer object
        root.appendChild(self._PyutActor2xml(oglActor.getPyutObject(), xmlDoc))

        return root

    
#>------------------------------------------------------------------------

    def _OglUseCase2xml(self, oglUseCase, xmlDoc):
        """
        Exporting an OglUseCase to an miniDom Element.

        @param OglUseCase oglUseCase : UseCase to convert
        @param xmlDoc : xml document
        @return Element : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        root = xmlDoc.createElement('GraphicUseCase')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglUseCase, root)

        # adding the data layer object
        root.appendChild(self._PyutUseCase2xml(oglUseCase.getPyutObject(), xmlDoc))

        return root

    
#>------------------------------------------------------------------------

    def save(self, oglObjects, umlFrame):
        """
        To save diagram in XML file.

        @author Deve Roux <droux@eivd.ch>
        @modified Laurent Burgbacher <lb@alawa.ch> : add version support
        """
        from xml.dom.minidom import Document
        xmlDoc    = Document()
        top     = xmlDoc.createElement("Pyut")
        top.setAttribute('version', str(THIS_VERSION))
        # version 1 is anything that has no version number...

        xmlDoc.appendChild(top)

        # Gauge
        dlg=wx.Dialog(None, -1, "Saving...",
                     style=wx.STAY_ON_TOP | wx.CAPTION | wx.THICK_FRAME,
                     size=wx.Size(207, 70))
        gauge=wx.Gauge(dlg, -1, len(oglObjects), pos=wx.Point(2, 5),
                      size=wx.Size(200, 30))
        dlg.Show(True)

        for i in range(len(oglObjects)):
            gauge.SetValue(i)
            if isinstance(oglObjects[i], OglClass):
                top.appendChild(self._OglClass2xml(oglObjects[i], xmlDoc))
            elif isinstance(oglObjects[i], OglNote):
                top.appendChild(self._OglNote2xml(oglObjects[i], xmlDoc))
            elif isinstance(oglObjects[i], OglActor):
                top.appendChild(self._OglActor2xml(oglObjects[i], xmlDoc))
            elif isinstance(oglObjects[i], OglUseCase):
                top.appendChild(self._OglUseCase2xml(oglObjects[i], xmlDoc))
            elif isinstance(oglObjects[i], OglLink):
                top.appendChild(self._OglLink2xml(oglObjects[i], xmlDoc))
        dlg.Destroy()

        return xmlDoc

#>------------------------------------------------------------------------
    #   Here begins reading file
#>------------------------------------------------------------------------

    def _getParam(self, Param):
        aParam = PyutParam()
        if(Param.hasAttribute('defaultValue')):
            aParam.setDefaultValue(Param.getAttribute('defaultValue'))
        aParam.setName(Param.getAttribute('name'))
        aParam.setType(Param.getAttribute('type'))
        return aParam

#>------------------------------------------------------------------------

    def _getMethods(self, Class):
        """
        To extract methods form interface.

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        # class methods for this currente class
        allMethods = []
        for Method in Class.getElementsByTagName("Method") :

            # method name
            aMethod = PyutMethod(Method.getAttribute('name'))

            # method visibility
            aMethod.setVisibility(Method.getAttribute('visibility'))


            # for method return type
            Return = Method.getElementsByTagName("Return")[0]
            aMethod.setReturns(Return.getAttribute('type'))

            # for methods param
            allParams = []
            for Param in  Method.getElementsByTagName("Param"):
                allParams.append(self._getParam(Param))


            # setting de params for thiy method
            aMethod.setParams(allParams)
            # hadding this method in all class methods
            allMethods.append(aMethod)

        return allMethods

#>------------------------------------------------------------------------

    def _getControlPoints(self, link):
        """
        To extract control points from links.

        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        # class methods for this currente class
        allControlPoints = []
        for cp in Class.getElementsByTagName('ControlPoint') :

            # point position
            x = cp.getAttribute('x')
            y = cp.getAttribute('y')

            point = ControlPoint(x, y)
            allControlPoints.append(point)

        return allControlPoints

#>------------------------------------------------------------------------

    def _getFields(self, Class):
        """
        To extract fields form Class.

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        # for class fields
        allFields = []
        for Field in Class.getElementsByTagName("Field"):

            aField = PyutField()
            aField.setVisibility(Field.getAttribute('visibility'))
            Param = Field.getElementsByTagName("Param")[0]
            if(Param.hasAttribute('defaultValue')):
                aField.setDefaultValue(Param.getAttribute('defaultValue'))
            aField.setName(Param.getAttribute('name'))
            aField.setType(Param.getAttribute('type'))

            allFields.append(aField)
        return allFields

#>------------------------------------------------------------------------

    def _getPyutLink(self, obj):
        """
        To extract a PyutLink from an OglLink object.

        @param String obj : Name of the object.
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        @changed Philippe Waelti <pwaelti@eivd.ch> : Refactoring campain
        @changed Laurent Burgbacher <lb@alawa.ch> : miniogl support
        """
        link = obj.getElementsByTagName("Link")[0]

        aLink = PyutLink()

        aLink.setBidir(int(link.getAttribute('bidir')))
        aLink.setDestCard(link.getAttribute('cardDestination'))
        aLink.setSrcCard(link.getAttribute('cardSrc'))
        aLink.setName(link.getAttribute('name'))
        aLink.setType(int(link.getAttribute('type')))
        # source and destination will be reconstructed by _getOglLinks

        sourceId = int(link.getAttribute('sourceId'))
        destId = int(link.getAttribute('destId'))

        return sourceId, destId, aLink

#>------------------------------------------------------------------------

    def _getOglLinks(self, xmlOglLinks, dicoOglObjects, dicoLink, \
            dicoFather, umlFrame):
        """
        To extract the links from an OGL object.

        @param String obj : Name of the object.
        @since 1.0
        @author Laurent Burgbacher <lb@alawa.ch>
        """
        for link in xmlOglLinks:
            # src and dst anchor position
            sx = float(link.getAttribute("srcX"))
            sy = float(link.getAttribute("srcY"))
            dx = float(link.getAttribute("dstX"))
            dy = float(link.getAttribute("dstY"))
            spline = int(link.getAttribute("spline"))

            # create a list of ControlPoints
            ctrlpts = []
            for ctrlpt in link.getElementsByTagName("ControlPoint"):
                x = float(ctrlpt.getAttribute("x"))
                y = float(ctrlpt.getAttribute("y"))
                ctrlpts.append(ControlPoint(x, y))

            # get the associated PyutLink
            srcId, dstId, pyutLink = self._getPyutLink(link)

            # create the OglLink
            oglLink = umlFrame.createNewLink(
                dicoOglObjects[srcId],
                dicoOglObjects[dstId],
                pyutLink.getType())
            oglLink.SetSpline(spline)

            # give it the PyutLink
            newPyutLink = oglLink.getPyutObject()
            # set the destination PyutObject
            newPyutLink.setDestination(dicoOglObjects[dstId].getPyutObject())
            newPyutLink.setSource(dicoOglObjects[srcId].getPyutObject())

            # copy the good information from the read link
            newPyutLink.setBidir(pyutLink.getBidir())
            newPyutLink.setDestCard(pyutLink.getDestCard())
            newPyutLink.setSrcCard(pyutLink.getSrcCard())
            newPyutLink.setName(pyutLink.getName())

            # put the anchors at the right position
            srcAnchor = oglLink.GetSource()
            dstAnchor = oglLink.GetDestination()
            srcAnchor.SetPosition(sx, sy)
            dstAnchor.SetPosition(dx, dy)

            # add the control points to the line
            line = srcAnchor.GetLines()[0] # only 1 line per anchor in pyut
            parent = line.GetSource().GetParent()
            selfLink = parent is line.GetDestination().GetParent()
            #print parent
            #print line.GetDestination().GetParent()
            for ctrl in ctrlpts:
                line.AddControl(ctrl)
                if selfLink:
                    x, y = ctrl.GetPosition()
                    ctrl.SetParent(parent)
                    ctrl.SetPosition(x, y)

            if isinstance(oglLink, OglAssociation):
                center = oglLink.getLabels()[CENTER]
                src = oglLink.getLabels()[SRC_CARD]
                dst = oglLink.getLabels()[DEST_CARD]

                label = link.getElementsByTagName("LabelCenter")[0]
                x = float(label.getAttribute("x"))
                y = float(label.getAttribute("y"))
                center.SetPosition(x, y)

                label = link.getElementsByTagName("LabelSrc")[0]
                x = float(label.getAttribute("x"))
                y = float(label.getAttribute("y"))
                src.SetPosition(x, y)

                label = link.getElementsByTagName("LabelDst")[0]
                x = float(label.getAttribute("x"))
                y = float(label.getAttribute("y"))
                dst.SetPosition(x, y)

#>------------------------------------------------------------------------

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
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
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

            # adding methods for this class
            pyutClass.setMethods(self._getMethods(xmlClass))

            # adding fields for this class
            pyutClass.setFields(self._getFields(xmlClass))

            dicoOglObjects[pyutClass.getId()] = oglClass

            # Adding OGL class to UML Frame
            x = float(xmlOglClass.getAttribute('x'))
            y = float(xmlOglClass.getAttribute('y'))
            umlFrame.addShape(oglClass, x, y)

#>------------------------------------------------------------------------

    def _getOglNotes(self, xmlOglNotes, dicoOglObjects, dicoLink, \
            dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT notes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglNotes : XML 'GraphicNote' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} fathers: Inheritance
        @param UmlFrame umlFrame : Where to draw
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        for xmlOglNote in xmlOglNotes:
            pyutNote = PyutNote()

            # Building OGL Note
            height = float(xmlOglNote.getAttribute('height'))
            width = float(xmlOglNote.getAttribute('width'))
            oglNote = OglNote(pyutNote, width, height)

            xmlNote = xmlOglNote.getElementsByTagName('Note')[0]

            pyutNote.setId(int(xmlNote.getAttribute('id')))

            # adding name for this class
            pyutNote.setName(xmlNote.getAttribute('name').encode("charmap"))

            # Update dicos
            dicoOglObjects[pyutNote.getId()] = oglNote

            # Update UML Frame
            x = float(xmlOglNote.getAttribute('x'))
            y = float(xmlOglNote.getAttribute('y'))
            umlFrame.addShape(oglNote, x, y)

#>------------------------------------------------------------------------

    def _getOglActors(self, xmlOglActors, dicoOglObjects, dicoLink, \
            dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT actors.

        @param Element[] xmlOglActors : XML 'GraphicActor' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} fathers: Inheritance
        @param UmlFrame umlFrame : Where to draw
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        for xmlOglActor in xmlOglActors:
            pyutActor = PyutActor()

            # Building OGL Actor
            height = float(xmlOglActor.getAttribute('height'))
            width = float(xmlOglActor.getAttribute('width'))
            oglActor = OglActor(pyutActor, width, height)

            xmlActor = xmlOglActor.getElementsByTagName('Actor')[0]

            pyutActor.setId(int(xmlActor.getAttribute('id')))

            # adding name for this class
            pyutActor.setName(xmlActor.getAttribute('name').encode("charmap"))

            # Update dicos
            dicoOglObjects[pyutActor.getId()] = oglActor

            # Update UML Frame
            x = float(xmlOglActor.getAttribute('x'))
            y = float(xmlOglActor.getAttribute('y'))
            umlFrame.addShape(oglActor, x, y)

#>------------------------------------------------------------------------

    def _getOglUseCases(self, xmlOglUseCases, dicoOglObjects, dicoLink, \
            dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT actors.

        @param Element[] xmlOglUseCases : XML 'GraphicUseCase' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} fathers: Inheritance
        @param UmlFrame umlFrame : Where to draw
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        for xmlOglUseCase in xmlOglUseCases:
            pyutUseCase = PyutUseCase()

            # Building OGL UseCase
            height = float(xmlOglUseCase.getAttribute('height'))
            width = float(xmlOglUseCase.getAttribute('width'))
            oglUseCase = OglUseCase(pyutUseCase, width, height)

            xmlUseCase = xmlOglUseCase.getElementsByTagName('UseCase')[0]

            pyutUseCase.setId(int(xmlUseCase.getAttribute('id')))

            # adding name for this class
            pyutUseCase.setName(\
                    xmlUseCase.getAttribute('name').encode("charmap"))

            # Update dicos
            dicoOglObjects[pyutUseCase.getId()] = oglUseCase

            # Update UML Frame
            x = float(xmlOglUseCase.getAttribute('x'))
            y = float(xmlOglUseCase.getAttribute('y'))
            umlFrame.addShape(oglUseCase, x, y)

#>------------------------------------------------------------------------

    def open(self, dom, umlFrame):
        """
        To open a file and creating diagram.

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        @modified Laurent Burgbacher <lb@alawa.ch> : version 2
        """
        root = dom.getElementsByTagName("Pyut")[0]
        if root.hasAttribute('version'):
            version = int(root.getAttribute("version"))
        else:
            version = 1
        if version != THIS_VERSION:
            print "Wrong version of the file loader"
            print "This is version", THIS_VERSION, "and the file version is",\
                version
            raise "VERSION_ERROR"

        dicoOglObjects = {}  # format {id/name : oglClass}
        dicoLink = {}   # format [id/name : PyutLink}
        dicoFather = {} # format {id child oglClass : [id fathers]}

        #Create and init gauge
        dlgGauge=wx.Dialog(None, -1, "Loading...",
                      style=wx.STAY_ON_TOP | wx.CAPTION | wx.THICK_FRAME,
                      size=wx.Size(207, 70))
        gauge=wx.Gauge(dlgGauge, -1, 5, pos=wx.Point(2, 5),
                      size=wx.Size(200, 30))
        dlgGauge.Show(True)

        # for all elements il xml file
        dlgGauge.SetTitle("Reading file...")
        gauge.SetValue(1)

        # Load OGL Classes
        self._getOglClasses(dom.getElementsByTagName('GraphicClass'),
            dicoOglObjects, dicoLink, dicoFather, umlFrame)

        # Load OGL Notes
        self._getOglNotes(dom.getElementsByTagName('GraphicNote'),
            dicoOglObjects, dicoLink, dicoFather, umlFrame)

        # Load OGL Actors
        self._getOglActors(dom.getElementsByTagName('GraphicActor'),
            dicoOglObjects, dicoLink, dicoFather, umlFrame)

        # Load OGL UseCases
        self._getOglUseCases(dom.getElementsByTagName('GraphicUseCase'),
            dicoOglObjects, dicoLink, dicoFather, umlFrame)

        # Load OGL Links
        self._getOglLinks(dom.getElementsByTagName("GraphicLink"),
            dicoOglObjects, dicoLink, dicoFather, umlFrame)

        # fix the link's destination field
        gauge.SetValue(2)
        dlgGauge.SetTitle("Fixing link's destination...")
        for links in dicoLink.values():
            for link in links:
                link[1].setDestination(dicoOglObjects[link[0]].getPyutObject())

        # adding fathers
        dlgGauge.SetTitle("Adding fathers...")
        gauge.SetValue(3)
        for child, fathers in dicoFather.items():
            for father in fathers:
                umlFrame.createInheritanceLink(\
                        dicoOglObjects[child], dicoOglObjects[father])


        # adding links to this OGL object
        dlgGauge.SetTitle("Adding Links...")
        gauge.SetValue(4)
        for src, links in dicoLink.items():
            for link in links:
                createdLink = umlFrame.createNewLink(dicoOglObjects[src], \
                    dicoOglObjects[link[1].getDestination().getId()], \
                    link[1].getType())

                # fix link with the loaded information
                pyutLink = createdLink.getPyutObject()
                pyutLink.setBidir(link[1].getBidir())
                pyutLink.setDestCard(link[1].getDestCard())
                pyutLink.setSrcCard(link[1].getSrcCard())
                pyutLink.setName(link[1].getName())


        # to draw diagram
        umlFrame.Refresh()
        gauge.SetValue(5)

        dlgGauge.Destroy()

    
#>------------------------------------------------------------------------

    def joli(self, fileName):
        """
        To open a file and creating diagram.

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        from StringIO import StringIO
        dom = parse(StringIO(open(fileName).read()))
        xml.dom.ext.PrettyPrint(dom, open("joli.xml", 'w'))

