#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.13 $"
__author__ = "EI5, eivd, Group Burgbacher - Waelti"
__date__ = "2002-1-9"

from PyutParam       import *
from PyutMethod      import *
from PyutField       import *
from PyutStereotype  import *
from PyutType        import *
from PyutConsts      import *
from PyutSDInstance  import *
from PyutSDMessage   import *

# reading file
from StringIO import StringIO
from UmlFrame import *
from OglClass import OglClass
from OglSDInstance import *
from OglSDMessage import *
from OglLink  import *
from OglAssociation import *
#import lang
import PyutXmlV6
import wx

def secure_int(x):
    if x is not None:
        return int(x)
    else:
        return 0


class PyutXml(PyutXmlV6.PyutXml):
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

    New in PyutXmlV6 :
    - Save Sequence diagrams

    :version: $Revision: 1.13 $
    :author: C.Dutoit
    :contact: dutoitc@hotmail.com
    """

    #>------------------------------------------------------------------------
    def __init__(self):
        """
        Constructor
        @author C.Dutoit
        """
        self._this_version = 7



#>------------------------------------------------------------------------

    def _PyutSDInstance2xml(self, pyutSDInstance, xmlDoc):
        """
        Exporting an PyutSDInstance to an miniDom Element.

        @param PyutMethod pyutClass : Class to save
        @param xmlDoc xml document
        @return Element : XML Node
        @author Deve Roux
        @modified C.Dutoit/20021121 added display properties
        """
        root = xmlDoc.createElement('SDInstance')

        # ID
        root.setAttribute('id', str(pyutSDInstance.getId()))

        # instance name
        root.setAttribute('instanceName', pyutSDInstance.getInstanceName())

        # lifeLine length
        root.setAttribute('lifeLineLength', str(pyutSDInstance.getInstanceLifeLineLength()))

        return root


#>------------------------------------------------------------------------

    def _OglSDInstance2xml(self, oglSDInstance, xmlDoc):
        """
        Exporting an OglSDInstance to a miniDom Element.

        @param OglSDInstance oglSDInstance : Instance to save
        @param xmlDoc xml document
        @return Element : XML Node
        @author C.Dutoit
        """
        root = xmlDoc.createElement('GraphicSDInstance')

        # Append OGL object base (size and pos)
        self._appendOglBase(oglSDInstance, root)

        # adding the data layer object
        root.appendChild(self._PyutSDInstance2xml(
                                    oglSDInstance.getPyutObject(), xmlDoc))

        return root


#>------------------------------------------------------------------------

    def _PyutSDMessage2xml(self, pyutSDMessage, xmlDoc):
        """
        Exporting an PyutSDMessage to an miniDom Element.

        @param PyutMethod pyutSDMessage : SDMessage to save
        @param xmlDoc xml document
        @return Element : XML Node
        @author C.Dutoit
        """
        root = xmlDoc.createElement('SDMessage')

        # ID
        root.setAttribute('id', str(pyutSDMessage.getId()))

        # message
        root.setAttribute('message', pyutSDMessage.getMessage())

        # time
        root.setAttribute('srcTime', str(pyutSDMessage.getSrcTime()))
        root.setAttribute('dstTime', str(pyutSDMessage.getDstTime()))
        root.setAttribute('srcID', str(pyutSDMessage.getSrcID()))
        root.setAttribute('dstID', str(pyutSDMessage.getDstID()))

        return root


#>------------------------------------------------------------------------

    def _OglSDMessage2xml(self, oglSDMessage, xmlDoc):
        """
        Exporting an OglSDMessage to an miniDom Element.

        @param PyutMethod oglSDMessage : Message to save
        @param xmlDoc xml document
        @return Element : XML Node
        @author C.Dutoit
        """
        root = xmlDoc.createElement('GraphicSDMessage')

        # Append OGL object base (size and pos)
        #self._appendOglBase(oglSDMessage, root)

        # adding the data layer object
        root.appendChild(self._PyutSDMessage2xml(oglSDMessage.getPyutObject(), xmlDoc))

        return root



#>------------------------------------------------------------------------
    #    Here begin saving file
#>------------------------------------------------------------------------



#>------------------------------------------------------------------------

    def _getOglSDInstances(self, xmlOglSDInstances, dicoOglObjects, dicoLink, \
            dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT classes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglSDInstancees : XML 'GraphicSDInstance' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} fathers: Inheritance
        @param UmlFrame umlFrame : Where to draw
        @author Philippe Waelti <pwaelti@eivd.ch>
        @modified C.Dutoit/20021121 added display properties
        """
        for xmlOglSDInstance in xmlOglSDInstances:
            # Main objects
            pyutSDInstance = PyutSDInstance()
            oglSDInstance = OglSDInstance(pyutSDInstance, umlFrame)

            # Data layer
            xmlSDInstance = xmlOglSDInstance.getElementsByTagName(
                                                            'SDInstance')[0]

            # Pyut Data
            pyutSDInstance.setId(int(xmlSDInstance.getAttribute('id')))
            pyutSDInstance.setInstanceName(xmlSDInstance.getAttribute(
                                            'instanceName').encode("charmap"))
            pyutSDInstance.setInstanceLifeLineLength(
                    secure_int(xmlSDInstance.getAttribute('lifeLineLength')))


            dicoOglObjects[pyutSDInstance.getId()] = oglSDInstance

            # Adding OGL class to UML Frame
            x = float(xmlOglSDInstance.getAttribute('x'))
            y = float(xmlOglSDInstance.getAttribute('y'))
            w = float(xmlOglSDInstance.getAttribute('width'))
            h = float(xmlOglSDInstance.getAttribute('height'))
            oglSDInstance.SetSize(w, h)
            umlFrame.addShape(oglSDInstance, x, y)


#>----------------------------------------------------------------------------

    def _getOglSDMessages(self, xmlOglSDMessages, dicoOglObjects, dicoLink, \
            dicoFather, umlFrame):
        """
        Parse the XML elements given and build data layer for PyUT classes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglSDInstances : XML 'GraphicSDInstance elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} fathers: Inheritance
        @param UmlFrame umlFrame : Where to draw
        @author Philippe Waelti <pwaelti@eivd.ch>
        @modified C.Dutoit/20021121 added display properties
        """
        for xmlOglSDMessage in xmlOglSDMessages:

            # Data layer class
            xmlPyutSDMessage = xmlOglSDMessage.getElementsByTagName('SDMessage')[0]

            # Building OGL
            pyutSDMessage = PyutSDMessage()
            srcID = int(xmlPyutSDMessage.getAttribute('srcID'))
            dstID = int(xmlPyutSDMessage.getAttribute('dstID'))
            srcTime = int(float(xmlPyutSDMessage.getAttribute('srcTime')))
            dstTime = int(float(xmlPyutSDMessage.getAttribute('dstTime')))
            srcOgl = dicoOglObjects[srcID]
            dstOgl = dicoOglObjects[dstID]
            oglSDMessage = OglSDMessage(srcOgl, pyutSDMessage, dstOgl)
            pyutSDMessage.setOglObject(oglSDMessage)
            pyutSDMessage.setSource(srcOgl.getPyutObject(), srcTime)
            pyutSDMessage.setDestination(dstOgl.getPyutObject(), dstTime)


            # Pyut Datas
            pyutSDMessage.setId(int(xmlPyutSDMessage.getAttribute('id')))
            pyutSDMessage.setMessage(xmlPyutSDMessage.getAttribute('message').encode("charmap"))

            dicoOglObjects[pyutSDMessage.getId()] = pyutSDMessage

            # Adding OGL class to UML Frame
            #x = float(xmlOglSDMessage.getAttribute('x'))
            #y = float(xmlOglSDMessage.getAttribute('y'))
            diagram = umlFrame.GetDiagram()
            dicoOglObjects[srcID].addLink(oglSDMessage)
            dicoOglObjects[dstID].addLink(oglSDMessage)
            diagram.AddShape(oglSDMessage)
            #umlFrame.addShape(oglSDMessage, x, y)


    #>------------------------------------------------------------------------

    def _PyutNote2xml(self, pyutNote, xmlDoc):
        """
        Exporting an PyutNote to an miniDom Element.

        @param PyutNote pyutNote : Note to convert
        @param xmlDoc : xml document
        @return Element          : New miniDom element
        @author Philippe Waelti
        @modified C.Dutoit 2002-12-26, added multiline support
        """
        from xml.dom.minidom import Element

        root = xmlDoc.createElement('Note')

        # ID
        root.setAttribute('id', str(pyutNote.getId()))

        # Note
        name = pyutNote.getName()
        name = name.replace('\n', "\\\\\\\\")
        root.setAttribute('name', name)

        # filename (added by LB)
        root.setAttribute('filename', pyutNote.getFilename())

        return root


    #>------------------------------------------------------------------------

    #def save(self, oglObjects, umlFrames):
    def save(self, project):
        """
        To save diagram in XML file.

        @param umlFrames : list of umlFrames

        @author Deve Roux
        @modified Laurent Burgbacher <lb@alawa.ch> : add version support
        @modified C.Dutoit 20021122 : added document container tag
        """
        from xml.dom.minidom import Document
        dlgGauge = None
        gauge = None
        try:
            xmlDoc  = Document()
            top     = xmlDoc.createElement("PyutProject")
            top.setAttribute('version', str(self._this_version))
            top.setAttribute('CodePath', project.getCodePath())

            xmlDoc.appendChild(top)

            # Gauge
            dlg=wx.Dialog(None, -1, "Saving...",
                         style=wx.STAY_ON_TOP | wx.CAPTION | wx.THICK_FRAME,
                         size=wx.Size(207, 70))
            gauge=wx.Gauge(dlg, -1, 100, pos=wx.Point(2, 5),
                          size=wx.Size(200, 30))
            dlg.Show(True)

            # Save all documents in the project
            for document in project.getDocuments():
                documentNode = xmlDoc.createElement("PyutDocument")
                documentNode.setAttribute('type', 
                                      diagramTypeAsString(document.getType()))
                top.appendChild(documentNode)

               
                oglObjects = document.getFrame().getUmlObjects()
                for i in range(len(oglObjects)):
                    gauge.SetValue(i*100/len(oglObjects))
                    oglObject = oglObjects[i]
                    if isinstance(oglObject, OglClass):
                        documentNode.appendChild(self._OglClass2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglNote):
                        documentNode.appendChild(self._OglNote2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglActor):
                        documentNode.appendChild(self._OglActor2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglUseCase):
                        documentNode.appendChild(self._OglUseCase2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglLink):
                        documentNode.appendChild(self._OglLink2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglSDInstance):
                        documentNode.appendChild(self._OglSDInstance2xml(oglObject, xmlDoc))
                    elif isinstance(oglObject, OglSDMessage):
                        documentNode.appendChild(self._OglSDMessage2xml(oglObject, xmlDoc))
        except:
            try:
                dlg.Destroy()
            except:
                pass
            displayError(_("Can't save file"))
            return xmlDoc

        dlg.Destroy()


        #for i in range(len(oglObjects)):
        #    gauge.SetValue(i)
        #    if isinstance(oglObjects[i], OglClass):
        #        top.appendChild(self._OglClass2xml(oglObjects[i]))
        #    elif isinstance(oglObjects[i], OglNote):
        #        top.appendChild(self._OglNote2xml(oglObjects[i]))
        #    elif isinstance(oglObjects[i], OglActor):
        #        top.appendChild(self._OglActor2xml(oglObjects[i]))
        #    elif isinstance(oglObjects[i], OglUseCase):
        #        top.appendChild(self._OglUseCase2xml(oglObjects[i]))
        #    elif isinstance(oglObjects[i], OglLink):
        #        top.appendChild(self._OglLink2xml(oglObjects[i]))

        return xmlDoc



#>------------------------------------------------------------------------
    #   Here begins reading file
#>------------------------------------------------------------------------

    def open(self, dom, project):
        """
        To open a file and creating diagram.

        @author Deve Roux
        @modified Laurent Burgbacher : version 2
        @modified C.Dutoit : version 5, 7
        """
        dlgGauge = None
        gauge = None
        try:
            root = dom.getElementsByTagName("PyutProject")[0]
            if root.hasAttribute('version'):
                version = int(root.getAttribute("version"))
            else:
                version = 1
            if version != self._this_version:
                print "Wrong version of the file loader"
                print "This is version", self._this_version, "and the file version is",\
                    version
                raise "VERSION_ERROR"
            project.setCodePath(root.getAttribute("CodePath"))



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

            for documentNode in dom.getElementsByTagName("PyutDocument"):
                dicoOglObjects = {}  # format {id/name : oglClass}
                dicoLink = {}   # format [id/name : PyutLink}
                dicoFather = {} # format {id child oglClass : [id fathers]}

                # Create document and umlframe
                type = documentNode.getAttribute("type").encode("charmap")
                document = project.newDocument(diagramTypeFromString(type))
                umlFrame = document.getFrame()
                import mediator
                ctrl = mediator.getMediator()
                ctrl.getFileHandling().showFrame(umlFrame)

                # Load OGL Classes
                self._getOglClasses(documentNode.getElementsByTagName('GraphicClass'),
                    dicoOglObjects, dicoLink, dicoFather, umlFrame)

                # Load OGL Notes
                self._getOglNotes(documentNode.getElementsByTagName('GraphicNote'),
                    dicoOglObjects, dicoLink, dicoFather, umlFrame)

                # Load OGL Actors
                self._getOglActors(documentNode.getElementsByTagName('GraphicActor'),
                    dicoOglObjects, dicoLink, dicoFather, umlFrame)

                # Load OGL UseCases
                self._getOglUseCases(documentNode.getElementsByTagName('GraphicUseCase'),
                    dicoOglObjects, dicoLink, dicoFather, umlFrame)

                # Load OGL Links
                self._getOglLinks(documentNode.getElementsByTagName("GraphicLink"),
                    dicoOglObjects, dicoLink, dicoFather, umlFrame)

                # Load OGL SDInstances
                self._getOglSDInstances(documentNode.getElementsByTagName("GraphicSDInstance"),
                    dicoOglObjects, dicoLink, dicoFather, umlFrame)

                # Load OGL SDMessage
                self._getOglSDMessages(documentNode.getElementsByTagName("GraphicSDMessage"),
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
        except:
            dlgGauge.Destroy()
            displayError(_("Can't load file"))
            umlFrame.Refresh()
            return



        # to draw diagram
        umlFrame.Refresh()
        gauge.SetValue(5)

        dlgGauge.Destroy()



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
        @author Philippe Waelti
        @modified C.Dutoit 2002-12-26, added multiline support
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
            name=xmlNote.getAttribute('name')
            name = name.replace("\\\\\\\\", "\n")
            pyutNote.setName(name.encode("charmap"))

            # adding associated filename (lb@alawa.ch)
            pyutNote.setFilename(xmlNote.getAttribute('filename'))

            # Update dicos
            dicoOglObjects[pyutNote.getId()] = oglNote

            # Update UML Frame
            x = float(xmlOglNote.getAttribute('x'))
            y = float(xmlOglNote.getAttribute('y'))
            umlFrame.addShape(oglNote, x, y)

