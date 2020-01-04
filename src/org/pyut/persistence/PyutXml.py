
from logging import Logger
from logging import getLogger

from xml.dom.minidom import Document

from org.pyut.PyutActor import PyutActor
from org.pyut.PyutClass import PyutClass
from org.pyut.PyutField import PyutField
from org.pyut.PyutLink import PyutLink
from org.pyut.PyutMethod import PyutMethod
from org.pyut.PyutNote import PyutNote
from org.pyut.PyutParam import PyutParam
from org.pyut.PyutStereotype import getPyutStereotype
from org.pyut.PyutUseCase import PyutUseCase
from org.pyut.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.ogl.OglActor import OglActor
from org.pyut.ogl.OglNote import OglNote
from org.pyut.ogl.OglObject import OglObject
from org.pyut.ogl.OglUseCase import OglUseCase
from org.pyut.ogl.OglClass import OglClass

from org.pyut.ui.UmlFrame import UmlFrame

import wx


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
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def open(self, dom, umlFrame):
        """
        To open a file and creating diagram.

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        dicoOglObjects = {}  # format {name : oglClass}
        dicoLink = {}        # format [name : PyutLink}
        dicoFather = {}      # format {child oglClass : [fathers names]}
        oldData = 0

        # Create and init gauge
        dlgGauge = wx.Dialog(None, -1, "Loading...", style=wx.STAY_ON_TOP | wx.CAPTION | wx.RESIZE_BORDER, size=wx.Size(207, 70))
        gauge = wx.Gauge(dlgGauge, -1, 5, pos=wx.Point(2, 5), size=wx.Size(200, 30))

        dlgGauge.Show(True)

        # for all elements il xml file
        dlgGauge.SetTitle("Reading file...")
        gauge.SetValue(1)

        # Load OGL Classes
        oldData += self._getOglClasses(dom.getElementsByTagName('GraphicClass'), dicoOglObjects, dicoLink, dicoFather, umlFrame)

        # Load OGL Notes
        oldData += self._getOglNotes(dom.getElementsByTagName('GraphicNote'), dicoOglObjects, dicoLink, dicoFather, umlFrame)

        # Load OGL Actors
        oldData += self._getOglActors(dom.getElementsByTagName('GraphicActor'), dicoOglObjects, dicoLink, dicoFather, umlFrame)

        # Load OGL UseCases
        oldData += self._getOglUseCases(dom.getElementsByTagName('GraphicUseCase'), dicoOglObjects, dicoLink, dicoFather, umlFrame)

        # Fix links destination IDs if old data
        if oldData > 0:
            self._fixVersion(dicoLink, dicoOglObjects, dicoFather)

        # fix the link's destination field
        gauge.SetValue(2)
        dlgGauge.SetTitle("Fixing link's destination...")
        for links in list(dicoLink.values()):
            for link in links:
                link[1].setDestination(dicoOglObjects[link[0]].getPyutObject())

        # adding fathers
        dlgGauge.SetTitle("Adding fathers...")
        gauge.SetValue(3)
        for child, fathers in list(dicoFather.items()):
            for father in fathers:
                umlFrame.createInheritanceLink(dicoOglObjects[child], dicoOglObjects[father])

        # adding links to this OGL object
        dlgGauge.SetTitle("Adding Links...")
        gauge.SetValue(4)
        for src, links in list(dicoLink.items()):
            for link in links:
                createdLink = umlFrame.createNewLink(dicoOglObjects[src],
                                                     dicoOglObjects[link[1].getDestination().getId()],
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

    # noinspection PyUnusedLocal
    def save(self, oglObjects, umlFrame):
        """
        To save save diagram in XML file.

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        root    = Document()
        top     = root.createElement("Pyut")
        root.appendChild(top)

        self.__savedLinks = {}

        # Gauge
        dlg = wx.Dialog(None, -1, "Saving...", style=wx.STAY_ON_TOP | wx.CAPTION, size=wx.Size(207, 70))
        gauge = wx.Gauge(dlg, -1, len(oglObjects), pos=wx.Point(2, 5), size=wx.Size(200, 30))
        dlg.Show(True)

        for i in range(len(oglObjects)):
            gauge.SetValue(i)
            if isinstance(oglObjects[i], OglClass):
                top.appendChild(self._OglClass2xml(oglObjects[i], root))
            elif isinstance(oglObjects[i], OglNote):
                top.appendChild(self._OglNote2xml(oglObjects[i], root))
            elif isinstance(oglObjects[i], OglActor):
                top.appendChild(self._OglActor2xml(oglObjects[i], root))
            elif isinstance(oglObjects[i], OglUseCase):
                top.appendChild(self._OglUseCase2xml(oglObjects[i], root))
        dlg.Destroy()

        self.__savedLinks = None
        return root

    def _appendLinks(self, pyutLinkedObject, root, xmlDoc):
        """
        Write the links connected to the PyutLinkedObject.

        @param PyutLinkedObject pyutLinkedObject : Object which contains
        @param xmlDoc : xml Document instance
        @param Element root : XML node to write
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # for all links
        for link in pyutLinkedObject.getLinks():
            xmlLink = self._PyutLink2xml(link, xmlDoc)
            if xmlLink is not None:
                root.appendChild(xmlLink)

    def _appendFathers(self, pyutLinkedObject, root, xmlDoc):
        """
        Write the inheritance links connected to the PyutLinkedObject.

        @param PyutLinkedObject pyutLinkedObject : Object which contains links
        @param Element root : XML node to write
        @param xmlDoc : xml Document instance
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # lang.importLanguage()
        # for all fathers
        for father in pyutLinkedObject.getParents():
            xmlFather = xmlDoc.createElement('Father')
            xmlFather.setAttribute('id', str(father.getId()))
            root.appendChild(xmlFather)

    def _PyutLink2xml(self, pyutLink, xmlDoc):
        """
        Exporting an PyutLink to an miniDom Element.

        @param PyutLink pyutLink : Link to save
        @param xmlDoc : xml Document instance
        @return Element : XML Node
        @since 2.0
        @author Deve Roux <droux@eivd.ch>
        """
        # lang.importLanguage()

        # Add link to saved links (avoid to save one twice)
        if pyutLink in self.__savedLinks:
            return None
        self.__savedLinks[pyutLink] = 1

        root = xmlDoc.createElement('Link')
        # link name
        root.setAttribute('name', pyutLink.getName())

        # link type
        root.setAttribute('type', str(pyutLink.getType()))

        # link cardinality source
        root.setAttribute('cardSrc', pyutLink.getSrcCard())

        # link cardinality destination
        root.setAttribute('cardDestination', pyutLink.getDestCard())

        # link bidir
        root.setAttribute('bidir', str(pyutLink.getBidir()))

        # link destination
        root.setAttribute('destination', pyutLink.getDestination().getName())
        root.setAttribute('destId', str(pyutLink.getDestination().getId()))

        return root

    def _PyutParam2xml(self, pyutParam, xmlDoc):
        """
        Exporting a PyutParam to an miniDom Element.

        @param PyutParam pyutParam : Parameters to save
        @param xmlDoc : xml Document instance
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
        if defaultValue is not None:
            root.setAttribute('defaultValue', defaultValue)

        return root

    def _PyutField2xml(self, pyutField, xmlDoc):
        """
        Exporting a PyutField to an miniDom Element

        @param PyutField pyutField : Field to save
        @param xmlDoc : xml Document instance
        @return Element : XML Node
        @since 2.0
        @author Deve Roux <droux@eivd.ch>
        """
        root = xmlDoc.createElement('Field')

        # adding the parent XML
        # pyutField is a param
        root.appendChild(self._PyutParam2xml(pyutField, xmlDoc))

        # field visibility
        root.setAttribute('visibility', str(pyutField.getVisibility()))

        return root

    def _PyutMethod2xml(self, pyutMethod, xmlDoc):
        """
        Exporting an PyutMethod to an miniDom Element.

        @param PyutMethod pyutMethod : Method to save
        @param xmlDoc : xml Document instance
        @return Element : XML Node
        @author Deve Roux <droux@eivd.ch>
        """
        root = xmlDoc.createElement('Method')

        # method name
        root.setAttribute('name', pyutMethod.getName())

        # method visibility
        visibility: PyutVisibilityEnum = pyutMethod.getVisibility()
        if visibility is not None:
            # root.setAttribute('visibility', str(visibility.getVisibility()))
            root.setAttribute('visibility', visibility.value)

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
        for param in pyutMethod.getParams():
            root.appendChild(self._PyutParam2xml(param, xmlDoc))

        return root

    def _PyutClass2xml(self, pyutClass: PyutClass, xmlDoc: Document):
        """
        Exporting an PyutClass to an miniDom Element.

        Args:
            pyutClass: Class to save
            xmlDoc: xml Document instance

        Returns: XML Node
        """

        root = xmlDoc.createElement('Class')

        # ID
        root.setAttribute('id', str(pyutClass.getId()))

        # class name
        root.setAttribute('name', pyutClass.getName())

        # class stereotype
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

        # Append fathers
        self._appendFathers(pyutLinkedObject=pyutClass, root=root, xmlDoc=xmlDoc)

        # Append links
        self._appendLinks(pyutLinkedObject=pyutClass, root=root, xmlDoc=xmlDoc)

        return root

    def _PyutNote2xml(self, pyutNote, xmlDoc):
        """
        Exporting an PyutNote to an miniDom Element.

        @param PyutNote pyutNote : Note to convert
        @param xmlDoc : xml Document instance
        @return Element          : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        root = xmlDoc.createElement('Note')

        # ID
        root.setAttribute('id', str(pyutNote.getId()))

        # Note
        root.setAttribute('name', pyutNote.getName())

        # Append fathers
        self._appendFathers(pyutLinkedObject=pyutNote, root=root, xmlDoc=xmlDoc)

        # Append links
        self._appendLinks(pyutLinkedObject=pyutNote, root=root, xmlDoc=xmlDoc)

        return root

    def _PyutActor2xml(self, pyutActor, xmlDoc):
        """
        Exporting an PyutActor to an miniDom Element.

        @param PyutNote pyutActor : Note to convert
        @param xmlDoc : xml Document instance
        @return Element : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # lang.importLanguage()

        root = xmlDoc.createElement('Actor')

        # ID
        root.setAttribute('id', str(pyutActor.getId()))

        # Note
        root.setAttribute('name', pyutActor.getName())

        # Append fathers
        self._appendFathers(pyutLinkedObject=pyutActor, root=root, xmlDoc=xmlDoc)

        # Append links
        self._appendLinks(pyutLinkedObject=pyutActor, root=root, xmlDoc=xmlDoc)

        return root

    def _PyutUseCase2xml(self, pyutUseCase, xmlDoc):
        """
        Exporting an PyutUseCase to an miniDom Element.

        @param PyutNote pyutUseCase : Note to convert
        @param xmlDoc : xml Document instance
        @return Element : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # lang.importLanguage()

        root = xmlDoc.createElement('UseCase')

        # ID
        root.setAttribute('id', str(pyutUseCase.getId()))

        # Note
        root.setAttribute('name', pyutUseCase.getName())

        # Append fathers
        self._appendFathers(pyutLinkedObject=pyutUseCase, root=root, xmlDoc=xmlDoc)

        # Append links
        self._appendLinks(pyutLinkedObject=pyutUseCase, root=root, xmlDoc=xmlDoc)

        return root

    def _appendOglBase(self, oglObject: OglObject, root):
        """
        Saves the position and size of the OGL object in XML node.

        @param OglObject oglObject : OGL Object
        @param Element root : XML node to write
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        # Saving size
        # w, h = oglObject.GetBoundingBoxMin()
        w, h = oglObject.GetSize()
        root.setAttribute('width', str(int(w)))
        root.setAttribute('height', str(int(h)))

        # Saving position
        # x = int(oglObject.GetX())
        # y = int(oglObject.GetY())
        x, y = oglObject.GetTopLeft()
        root.setAttribute('x', str(x))
        root.setAttribute('y', str(y))

    def _OglClass2xml(self, oglClass: OglClass, xmlDoc):
        """
        Exporting an OglClass to an miniDom Element.

        @param PyutMethod oglClass : Class to save
        @param xmlDoc : xml Document instance
        @return Element : XML Node
        @author Deve Roux <droux@eivd.ch>
        """
        # lang.importLanguage()
        root = xmlDoc.createElement("GraphicClass")

        # Append OGL object base (size and pos)
        self._appendOglBase(oglClass, root)

        # adding the data layer object
        root.appendChild(self._PyutClass2xml(oglClass.getPyutObject(), xmlDoc))

        return root

    def _OglNote2xml(self, oglNote, xmlDoc):
        """
        Exporting an OglNote to an miniDom Element.

        @param OglNote oglNote : Note to convert
        @param xmlDoc : xml Document instance
        @return Element        : New miniDom element
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # lang.importLanguage()
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
        @param xmlDoc : xml Document instance
        @return Element : New miniDom element
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # lang.importLanguage()
        root = xmlDoc.createElement('GraphicActor')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglActor, root)

        # adding the data layer object
        root.appendChild(self._PyutActor2xml(oglActor.getPyutObject(), xmlDoc))

        return root

    def _OglUseCase2xml(self, oglUseCase, xmlDoc):
        """
        Exporting an OglUseCase to an miniDom Element.

        @param OglUseCase oglUseCase : UseCase to convert
        @param xmlDoc : xml Document instance
        @return Element : New miniDom element
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # lang.importLanguage()
        root = xmlDoc.createElement('GraphicUseCase')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglUseCase, root)

        # adding the data layer object
        root.appendChild(self._PyutUseCase2xml(oglUseCase.getPyutObject(),
                                               xmlDoc))

        return root

    def _getParam(self, Param):
        aParam = PyutParam()
        if Param.hasAttribute('defaultValue'):
            aParam.setDefaultValue(Param.getAttribute('defaultValue'))
        aParam.setName(Param.getAttribute('name'))
        aParam.setType(Param.getAttribute('type'))
        return aParam

    def _getMethods(self, Class):
        """
        To extract methods form interface.

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        # class methods for this currente class
        allMethods = []
        for Method in Class.getElementsByTagName("Method"):

            # method name
            aMethod = PyutMethod(Method.getAttribute('name'))

            # method visibility
            aMethod.setVisibility(Method.getAttribute('visibility'))

            # for method return type
            Return = Method.getElementsByTagName("Return")[0]
            aMethod.setReturns(Return.getAttribute('type'))

            # for methods param
            allParams = []
            for Param in Method.getElementsByTagName("Param"):
                allParams.append(self._getParam(Param))

            # setting de params for thiy method
            aMethod.setParams(allParams)
            # hadding this method in all class methods
            allMethods.append(aMethod)

        return allMethods

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
            # aField.setVisibility(Field.getAttribute('visibility'))
            vis: PyutVisibilityEnum = PyutVisibilityEnum(Field.getAttribute('visibility'))
            aField.setVisibility(vis)
            Param = Field.getElementsByTagName("Param")[0]
            if Param.hasAttribute('defaultValue'):
                aField.setDefaultValue(Param.getAttribute('defaultValue'))
            aField.setName(Param.getAttribute('name'))
            aField.setType(Param.getAttribute('type'))

            allFields.append(aField)
        return allFields

    def _getFathers(self, fathers, dicoFather, objectId):
        """
        To extract fathers form Class.

        @param  [] fathers
        @param {} dicoFather : {id / child name : [father name/id]}
        @param int objectId : child object id (or name)
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        if len(fathers) > 0:
            fathersIds = []
            for father in fathers:
                if father.hasAttribute('id'):
                    fathersIds.append(int(father.getAttribute('id')))
                else:
                    fathersIds.append(father.getAttribute('name').encode("charmap"))

            dicoFather[objectId] = fathersIds

    def _getLinks(self, obj):
        """
        To extract links form an OGL object.

        @param String obj : Name of the object.
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        @changed Philippe Waelti <pwaelti@eivd.ch> : Refactoring campain
        """
        allLinks = []
        for link in obj.getElementsByTagName("Link"):

            aLink = PyutLink()

            aLink.setBidir(bool(link.getAttribute('bidir')))
            aLink.setDestCard(link.getAttribute('cardDestination'))
            aLink.setSrcCard(link.getAttribute('cardSrc'))
            aLink.setName(link.getAttribute('name'))
            aLink.setType(link.getAttribute('type'))
            aLink.setDestination(link.getAttribute('destination'))

            # Backward compatibility
            if link.hasAttribute('destId'):
                destId = int(link.getAttribute('destId'))
            else:
                destId = 0

            allLinks.append([destId, aLink])

        return allLinks

    def _getOglClasses(self, xmlOglClasses, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT classes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglClasses : XML 'GraphicClass' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} dicoFather: Inheritance
        @param UmlFrame umlFrame : Where to draw
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        oldData = 0

        for xmlOglClass in xmlOglClasses:

            pyutClass = PyutClass()
            # Building OGL class
            height = int(xmlOglClass.getAttribute('height'))
            width = int(xmlOglClass.getAttribute('width'))
            oglClass = OglClass(pyutClass, width, height)

            # Data layer class
            xmlClass = xmlOglClass.getElementsByTagName('Class')[0]

            # Backward compatibility (pyut v1.0). If id not present,
            # auto set by the instanciation of object
            if xmlClass.hasAttribute('id'):
                pyutClass.setId(int(xmlClass.getAttribute('id')))
            else:
                oldData = 1

            # adding name for this class
            pyutClass.setName(xmlClass.getAttribute('name').encode("charmap"))

            # adding description
            pyutClass.setDescription(xmlClass.getAttribute('description'))

            # adding stereotype
            if xmlClass.hasAttribute('stereotype'):
                pyutClass.setStereotype(getPyutStereotype(xmlClass.getAttribute('stereotype')))

            # adding methods for this class
            pyutClass.setMethods(self._getMethods(xmlClass))

            # adding fields for this class
            pyutClass.setFields(self._getFields(xmlClass))

            # adding fathers
            self._getFathers(xmlClass.getElementsByTagName("Father"), dicoFather, pyutClass.getId())

            # adding link for this class
            dicoLink[pyutClass.getId()] = self._getLinks(xmlClass)[:]

            dicoOglObjects[pyutClass.getId()] = oglClass

            # Adding OGL class to UML Frame
            x = int(xmlOglClass.getAttribute('x'))
            y = int(xmlOglClass.getAttribute('y'))
            umlFrame.addShape(oglClass, x, y)

        return oldData

    def _getOglNotes(self, xmlOglNotes, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT notes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglNotes : XML 'GraphicNote' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} dicoFather: Inheritance
        @param UmlFrame umlFrame : Where to draw
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        oldData = 0

        for xmlOglNote in xmlOglNotes:
            pyutNote = PyutNote()

            # Building OGL Note
            height = int(xmlOglNote.getAttribute('height'))
            width = int(xmlOglNote.getAttribute('width'))
            oglNote = OglNote(pyutNote, width, height)

            xmlNote = xmlOglNote.getElementsByTagName('Note')[0]

            # Backward compatibility (pyut v1.0). If id not present,
            # auto set by the instanciation of object
            if xmlNote.hasAttribute('id'):
                pyutNote.setId(int(xmlNote.getAttribute('id')))
            else:
                oldData = 1

            # adding name for this class
            pyutNote.setName(xmlNote.getAttribute('name').encode("charmap"))

            # adding fathers
            self._getFathers(xmlNote.getElementsByTagName("Father"), dicoFather, pyutNote.getId())

            # Update dicos
            dicoLink[pyutNote.getId()] = self._getLinks(xmlNote)
            dicoOglObjects[pyutNote.getId()] = oglNote

            # Update UML Frame
            x = int(xmlOglNote.getAttribute('x'))
            y = int(xmlOglNote.getAttribute('y'))
            umlFrame.addShape(oglNote, x, y)

        return oldData

    def _getOglActors(self, xmlOglActors, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT actors.

        @param Element[] xmlOglActors : XML 'GraphicActor' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} dicoFather: Inheritance
        @param UmlFrame umlFrame : Where to draw
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        oldData = 0

        for xmlOglActor in xmlOglActors:
            pyutActor = PyutActor()

            # Building OGL Actor
            height = int(xmlOglActor.getAttribute('height'))
            width = int(xmlOglActor.getAttribute('width'))
            oglActor = OglActor(pyutActor, width, height)

            xmlActor = xmlOglActor.getElementsByTagName('Actor')[0]

            # Backward compatibility (pyut v1.0). If id not present,
            # auto set by the instanciation of object
            if xmlActor.hasAttribute('id'):
                pyutActor.setId(int(xmlActor.getAttribute('id')))
            else:
                oldData = 1

            # adding name for this class
            pyutActor.setName(xmlActor.getAttribute('name').encode("charmap"))

            # adding fathers
            self._getFathers(xmlActor.getElementsByTagName("Father"), dicoFather, pyutActor.getId())

            # Update dicos
            dicoLink[pyutActor.getId()] = self._getLinks(xmlActor)
            dicoOglObjects[pyutActor.getId()] = oglActor

            # Update UML Frame
            x = int(xmlOglActor.getAttribute('x'))
            y = int(xmlOglActor.getAttribute('y'))
            umlFrame.addShape(oglActor, x, y)

        return oldData

    def _getOglUseCases(self, xmlOglUseCases, dicoOglObjects, dicoLink, dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT actors.

        @param Element[] xmlOglUseCases : XML 'GraphicUseCase' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} dicoFather: Inheritance
        @param UmlFrame umlFrame : Where to draw
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        oldData = 0

        for xmlOglUseCase in xmlOglUseCases:
            pyutUseCase = PyutUseCase()

            # Building OGL UseCase
            height = int(xmlOglUseCase.getAttribute('height'))
            width = int(xmlOglUseCase.getAttribute('width'))
            oglUseCase = OglUseCase(pyutUseCase, width, height)

            xmlUseCase = xmlOglUseCase.getElementsByTagName('UseCase')[0]

            # Backward compatibility (pyut v1.0). If id not present,
            # auto set by the instanciation of object
            if xmlUseCase.hasAttribute('id'):
                pyutUseCase.setId(int(xmlUseCase.getAttribute('id')))
            else:
                oldData = 1

            # adding name for this class
            s = xmlUseCase.getAttribute('name').encode("charmap")
            pyutUseCase.setName(s)

            # adding fathers
            self._getFathers(xmlUseCase.getElementsByTagName("Father"), dicoFather, pyutUseCase.getId())

            # Update dicos
            dicoLink[pyutUseCase.getId()] = self._getLinks(xmlUseCase)
            dicoOglObjects[pyutUseCase.getId()] = oglUseCase

            # Update UML Frame
            x = int(xmlOglUseCase.getAttribute('x'))
            y = int(xmlOglUseCase.getAttribute('y'))
            umlFrame.addShape(oglUseCase, x, y)

        return oldData

    def _fixVersion(self, dicoLink, dicoOglObjects, dicoFather):
        """
        Fix links if old version of pyut (v1.0) has been detected.
        It replace the name in dicos with id's.

        @param {srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {srcName, OglLink} dicoLink : OGL links loaded
        @param {childName, fathers[]} dicoFather : Fathers of a class
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """
        # This works because destinaton of link is the NAME of dest
        # This is fixed just below
        for links in list(dicoLink.values()):
            for link in links:
                for objId, oglObject in list(dicoOglObjects.items()):
                    try:
                        if link[1].getDestination() == oglObject.getPyutObject().getName():
                            link[0] = objId
                    except (ValueError, Exception) as e:
                        # print(f"Error converting old data: {e}")
                        # print(link[1].getDestination(), end=' ')
                        # print(" == ", end=' ')
                        # print(oglObject.getPyutObject().getName())

                        self.logger.error(f"Error converting old data: {e}")
                        self.logger.error(f'{link[1].getDestination()} == {oglObject.getPyutObject().getName()}')

        for fathers in list(dicoFather.values()):
            for father in range(len(fathers)):
                for objId, oglObject in list(dicoOglObjects.items()):
                    if fathers[father] == oglObject.getPyutObject().getName():
                        fathers[father] = objId
