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
import PyutXmlV5
import wx


class PyutXml(PyutXmlV5.PyutXml):
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

    New in PyutXmlV5 :
    - Save documents

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
        self._this_version = 6


#>------------------------------------------------------------------------
    #    Here begin saving file
#>------------------------------------------------------------------------


    #def save(self, oglObjects, umlFrames):
    def save(self, project):
        """
        To save diagram in XML file.

        @param umlFrames : list of umlFrames

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        @modified Laurent Burgbacher <lb@alawa.ch> : add version support
        @modified C.Dutoit 20021122 : added document container tag
        """
        from xml.dom.minidom import Document
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

        return root



#>------------------------------------------------------------------------
    #   Here begins reading file
#>------------------------------------------------------------------------

    def open(self, dom, project):
        """
        To open a file and creating diagram.

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        @modified Laurent Burgbacher <lb@alawa.ch> : version 2
        @modified C.Dutoit : version 5
        """
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
            type = documentNode.getAttribute("type")
            document = project.newDocument(diagramTypeFromString(type))
            umlFrame = document.getFrame()

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

