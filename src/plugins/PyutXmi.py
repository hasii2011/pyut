#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.6 $"
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
import wx

class PyutXmi:
    """
    Class for saving and loading a UMI diagram.
    This class offers two main methods that are save() and open().
    Using the dom XMI model, you can, with the saving method, get the
    diagram corresponding XMI view. For loading, you have to parse
    the file and indicate the UML frame on which you want to draw
    (See `UmlFrame`).
    This file format is portable with authers UML tool like (Rational Rose)

    Sample use::

#XXX
#        # Write
#        pyutXmi = PyutXmi()
#        text = pyutXmi.save(oglObjects)
#        file.write(text)

        # open 
        dom = parse(StringIO(open(filename).read())) 

        myXmi = PyutXmi()
        myXmi.open(dom, umlFrame)

    :version: $Revision: 1.6 $
    :author: Deve Roux 
    :contact: droux@eivd.ch 
    @modified C.Dutoit feb 2003 : updated, fixed, improved
    """

    #>------------------------------------------------------------------------
    #    Here begin saving file
    #>------------------------------------------------------------------------

    def _PyutLink2xml(self, pyutLink):
        """
        Exporting an PyutLink to an miniDom Element 

        @since 2.0
        @Deve Roux <droux@eivd.ch>

        @param PyutLink  
        @return Element
        """

        # hadding links in dictionnary
        if pyutLink in self.__savedLinks:
            return None
        self.__savedLinks[pyutLink] = 1


        root = Element('Link')
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

        # link destination 
        root.setAttribute('destination', pyutLink.getDestination().getName()) 

        return root 

    #>------------------------------------------------------------------------

    def _PyutParam2xml(self, pyutParam):
        """
        Exporting an PyutParam to an miniDom Element 

        @since 2.0
        @Deve Roux <droux@eivd.ch>

        @param PyutParam  
        @return Element
        """
        root = Element('Param')

        # param name
        root.setAttribute('name', pyutParam.getName() ) 

        # param type
        root.setAttribute('type', str(pyutParam.getType())) 

        # param defaulf value
        defaultValue = pyutParam.getDefaultValue()
        if (defaultValue != None):
            root.setAttribute('defaultValue', defaultValue) 

        return root

    #>------------------------------------------------------------------------

    def _PyutField2xml(self, pyutField):
        """
        Exporting an PyutField to an miniDom Element 

        @since 2.0
        @Deve Roux <droux@eivd.ch>

        @param PyutField  
        @return Element
        """
        root = Element('Field')

        # adding the parent XML
        # pyutField is a param 
        root.appendChild(self._PyutParam2xml(pyutField))

        # field visibility        
        root.setAttribute('visibility', str(pyutField.getVisibility()) )

        return root

    #>------------------------------------------------------------------------

    def _PyutMethod2xml(self, pyutMethod):
        """
        Exporting an PyutMethod to an miniDom Element 

        @since 2.0
        @Deve Roux <droux@eivd.ch>

        @param PyutMethod  
        @return Element
        """
        root = Element('Method')

        # method name
        root.setAttribute('name', pyutMethod.getName() )

        # method visibility
        visibility = pyutMethod.getVisibility() 
        if (visibility != None):
            root.setAttribute('visibility', str(visibility.getVisibility())) 

        # for all modifiers
        for i in pyutMethod.getModifiers():
            modifier = Element('Modifier')
            modifier.setAttribute('name', i.getName()) 
            root.appendChild(modifier)


        # method return type 
        ret = pyutMethod.getReturns()
        if (ret != None):
            eleRet = Element('Return')
            eleRet.setAttribute('type', str(ret)) 
            root.appendChild(eleRet)

        # method params 
        for para in pyutMethod.getParams() :
            root.appendChild(self._PyutParam2xml(para))

        return root

    #>------------------------------------------------------------------------

    def _PyutClass2xml(self, pyutClass):
        """
        Exporting an PyutClass to an miniDom Element 

        @since 2.0
        @Deve Roux <droux@eivd.ch>

        @param PyutClass  
        @return Element
        """
        root = Element('Class')

        # class name
        root.setAttribute('name', pyutClass.getName())

        # classs stereotype
        stereotype = pyutClass.getStereotype()
        if (stereotype != None):
            root.setAttribute('stereotype', \
                              stereotype.getStereotype())

        # methods methods
        for i in pyutClass.getMethods():
            root.appendChild(self._PyutMethod2xml(i))

        # for all the field
        for i in pyutClass.getFields():
            root.appendChild(self._PyutField2xml(i))

        # for fathers
        fathers = pyutClass.getFathers()
        if(len(fathers) > 0):
            for i in fathers:
                father = Element('Father')
                father.setAttribute('name', i.getName() )
                root.appendChild(father)

        # for all links
        links = pyutClass.getLinks()
        for i in links:
            res = self._PyutLink2xml(i)
            if res is not None:
                root.appendChild(res)

        return root

    #>------------------------------------------------------------------------

    def _OglClass2xml(self, oglClass):
        """
        Exporting an OglClass to an miniDom Element 

        @since 2.0
        @Deve Roux <droux@eivd.ch>

        @param OglClass  
        @return Element
        """
        root = Element('GraphicClass')

        # class definition
        # adding width and height
        w, h = oglClass.GetBoundingBoxMin()
        root.setAttribute('width', str(int(w)) )
        root.setAttribute('height', str(int(h)) )

        # calculate the top right corner of the shape
        x = int(oglClass.GetX())
        y = int(oglClass.GetY())
        root.setAttribute('x', str(int(x)) )
        root.setAttribute('y', str(int(y)) )

        # adding the class
        root.appendChild(self._PyutClass2xml(oglClass.getPyutClass()))

        return root

    #>------------------------------------------------------------------------

    def save(self, oglObjects):
        """
        To save save diagram in XML file.

        @since 1.0
        @Deve Roux <droux@eivd.ch>
        """
        root    = Document()
        top     = Element("Pyut")
        root.appendChild(top)

        self.__savedLinks = {}

        #gauge
        dlg=wx.Dialog(NULL, -1, "Saving...", 
                     style=wx.STAY_ON_TOP | wx.CAPTION | wx.THICK_FRAME,
                     size=wx.Size(207, 70))
        gauge=wx.Gauge(dlg, -1, len(oglObjects), pos=wx.Point(2, 5),
                      size=wx.Size(200, 30))
        dlg.Show(True)
        for i in range(len(oglObjects)):
            gauge.SetValue(i)
            top.appendChild(self._OglClass2xml(oglObjects[i]))
        dlg.Destroy()
 
        self.__savedLinks = None 
        return root


    #>------------------------------------------------------------------------
    #   Here begin reading file
    #>------------------------------------------------------------------------

    def _xmiVisibility2PyutVisibility(self, visibility="private"):
        """
        To translate Xmi visibility to Pyut visibility.
        Translating :
            - private   -> -
            - public    -> +
            - protected -> #
            - others    -> 

        @param   String : Xmi  visibility
        @return  Sting  : Pyut visibility 

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        if(visibility == "private") :
            return "-"
        elif(visibility == "public") :
            return "+"
        elif(visibility == "protected") :
            return "#"
        
        return ""

    #>------------------------------------------------------------------------

    def _getDefaultValue(self, xmiParam, pyutParam) :
        """
        Get the default value from xmiParm and update pyutParam with
        the default value.

        @param   minidom.Element : xmiParam
        @param   PyutParam       : pyutParam

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        # get the value
        value = xmiParam.getElementsByTagName \
            ("Foundation.Data_Types.Expression.body")[0].firstChild

        if(value is not None):
            if(value.nodeType == value.TEXT_NODE) :
                # updating pyutParam  
                pyutParam.setDefaultValue(value.data)

    #>------------------------------------------------------------------------

    def _getType(self, dom) :
        """
        Parse dom document for all type ID  and update methods and params

        @param   minidom    : dom 

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        # parse to find type name using tag name
        def parse(dom, tag):
            for type in dom.getElementsByTagName(tag):
                id = type.getAttribute("xmi.id") 
                xmiType = type.getElementsByTagName("Foundation.Core.ModelElement.name")
                if(len(xmiType) > 0):
                    typeName = xmiType[0].firstChild.data
                    # making link with dictionnary
                    if(self.dicoType.has_key(id)):
                        self.dicoType[id].setType(typeName)
                    if(self.dicoReturn.has_key(id)):
                        self.dicoReturn[id].setReturns(typeName)

        parse(dom, "Foundation.Core.DataType")
        parse(dom,"Foundation.Data_Types.Enumeration")


    def _getTypeId(self, xmiParam, param, dico):
        """
        Parse xmiParam and making link in dico between param and xmiParam Id. 

        @param   xmiParam    : xmiParam 
        @param   PyutParam   : param 
        @param   {}          : dico : dicoType of dicoReturn

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        def parse(xmiParam, param, dico, tag):
            for type in xmiParam.getElementsByTagName(tag):
                id = type.getAttribute("xmi.idref") 
                dico[id] = param
        parse(xmiParam, param, dico, "Foundation.Core.DataType")
        parse(xmiParam, param, dico, "Foundation.Data_Types.Enumeration")

    #>------------------------------------------------------------------------

    def _getParam(self, Param, pyutMethod):
        """
        Extract param from Xmi file from Class part.
            
        @param   minidom.Element  : Param
        @param   pyutMethod for returned type 
        @return  PyutParam

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        aParam = PyutParam()

        # param's name
        name = Param.getElementsByTagName \
            ("Foundation.Core.ModelElement.name")[0].firstChild
        if(name.nodeType == name.TEXT_NODE) :
            if(name.data[-6:] == "Return"):
                self._getTypeId(Param, pyutMethod, self.dicoReturn)
                return None
            else:
                aParam.setName(name.data)

        # default value
        self._getDefaultValue(Param, aParam)

        # for type
        self._getTypeId(Param, aParam, self.dicoType)

        return  aParam

    #>------------------------------------------------------------------------

    def _getMethods(self, Class):
        """
        Extract method from Xmi file from Class part.

        @param   minidom.Element  : Class 
        @return  [] with PyutMethod 

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        # class methods for this currente class
        allMethods = []

        for Method in Class.getElementsByTagName("Foundation.Core.Operation") :

            # method name
            name = Method.getElementsByTagName \
                ("Foundation.Core.ModelElement.name")[0].firstChild
            if(name.nodeType == name.TEXT_NODE) :
                aMethod = PyutMethod(name.data)


                # method visibility
                visibility = Method.getElementsByTagName \
                    ("Foundation.Core.ModelElement.visibility")[0]
                aMethod.setVisibility(self._xmiVisibility2PyutVisibility\
                    (visibility.getAttribute('xmi.value')))


                # for methods param
                allParams = []
                for Param in Method.getElementsByTagName \
                        ("Foundation.Core.Parameter") :
                    pyutParam = self._getParam(Param, aMethod)
                    if(pyutParam is not None):
                        allParams.append(pyutParam)


                # setting de params for thiy method
                aMethod.setParams(allParams)

            # hadding this method in all class methods
            allMethods.append(aMethod)

        return allMethods

    #>------------------------------------------------------------------------

    def _getFields(self, Class):
        """
        To extract fields form Class.

        @param   minidom.Element  : Class 
        @return  [] with PyutField 

        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        # for class fields
        allFields = []


        for Field in Class.getElementsByTagName("Foundation.Core.Attribute") :
            aField = PyutField()

            # name
            name = Field.getElementsByTagName \
                ("Foundation.Core.ModelElement.name")[0].firstChild
            if(name.nodeType == name.TEXT_NODE) :
                aField.setName(name.data)

            # field visibility
            visibility = Field.getElementsByTagName \
                ("Foundation.Core.ModelElement.visibility")[0]
            aField.setVisibility(self._xmiVisibility2PyutVisibility\
                (visibility.getAttribute('xmi.value')))

            # default value
            self._getDefaultValue(Field, aField)


            # for type
            self._getTypeId(Field, aField, self.dicoType)


            allFields.append(aField)
        return allFields

    #>------------------------------------------------------------------------

    def _getFathers(self, dom, umlFrame):
        """
        To extract fathers form Class.

        @param xml.dom.minidom Element  : dom
        @param UmlFrame umlFrame 
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        # find id from class in src
        def parse(src, type):
            father = fathers.getElementsByTagName(type)
            if len(father)>0:
                klass =  father[0].getElementsByTagName\
                    ("Foundation.Core.Class")[0].getAttribute("xmi.idref")
                return klass

            return None

            
            
        # for all fathers links
        for fathers in dom.getElementsByTagName("Foundation.Core.Generalization"):

            # link id
            linkId = fathers.getAttribute("xmi.id")
            if(linkId != ""):
                print linkId

                father = parse(fathers, "Foundation.Core.Generalization.supertype")
                son    = parse(fathers, "Foundation.Core.Generalization.subtype")


                # find class with id
                pyutFather = self.dicoFather[linkId][father]
                pyutSon    = self.dicoFather[linkId][son]

                # Adding father in pyutClass
                pyutSon.getPyutObject().addFather(pyutFather)

                # hadding link in uml frame
                umlFrame.createInheritanceLink(pyutSon, pyutFather)

    #>------------------------------------------------------------------------

    def _getLinks(self, dom, umlFrame):
        """
        To extract links form an OGL object.

        @param xml.dom.minidom Element  : dom
        @param UmlFrame umlFrame 
        @since 1.0
        @author Deve Roux <droux@eivd.ch>
        """
        for association in dom.getElementsByTagName("Foundation.Core.Association"):
            
            linkId = association.getAttribute("xmi.id")
            if(linkId == ""):
                return
            print "liinId " + linkId

            linkName = ""
            xmiName = association.getElementsByTagName\
                ("Foundation.Core.ModelElement.name")
            if(len(xmiName)>0):
                name = xmiName[0].firstChild
                if name is not None:
                    if(name.nodeType == name.TEXT_NODE) :
                        linkName = name.data
            print "link name : "+linkName


            src = None
            dest = None
            for extremite in association.getElementsByTagName\
                ("Foundation.Core.AssociationEnd"):
                classId = extremite.getAttribute("xmi.id")
                if(not src):
                    src = self.dicoLinks[classId]

                else:
                    dest = self.dicoLinks[classId]

            type = OGL_ASSOCIATION 
            xmiType = association.getElementsByTagName("Foundation.Core.AssociationEnd.aggregation")
            if(xmiType[0].getAttribute("xmi.value")=='shared'):
                type = OGL_AGGREGATION
                

            createdLink = umlFrame.createNewLink(src, dest, type)
            createdLink.setName(linkName)
            createdLink.setDestination(src.getPyutObject())
                

          #<Foundation.Core.Association.connection>
          #  <Foundation.Core.AssociationEnd xmi.id = 'G.3'>
          #    <Foundation.Core.ModelElement.name>roleA</Foundation.Core.ModelElement.name>
          #    <Foundation.Core.ModelElement.visibility xmi.value = 'public'/>
          #    <Foundation.Core.AssociationEnd.isNavigable xmi.value = 'True'/>
          #    <Foundation.Core.AssociationEnd.isOrdered xmi.value = 'False'/>
          #    <Foundation.Core.AssociationEnd.aggregation xmi.value = 'none'/>
          #    <Foundation.Core.AssociationEnd.multiplicity>0..*</Foundation.Core.AssociationEnd.multiplicity>
          #    <Foundation.Core.AssociationEnd.changeable xmi.value = 'none'/>
          #    <Foundation.Core.AssociationEnd.targetScope xmi.value = 'instance'/>
          #    <Foundation.Core.AssociationEnd.type>
          #      <Foundation.Core.Class xmi.idref = 'S.10001'/> <!-- A -->
          #    </Foundation.Core.AssociationEnd.type>
          #  </Foundation.Core.AssociationEnd>
    #>------------------------------------------------------------------------

    def _getOglClasses(self, xmlOglClasses, dicoOglObjects, \
            umlFrame, oldData):
        """
        Parse the XMI elements given and build data layer for PyUT classes.
        If file is version 1.0, the dictionary given will contain, for key,
        the name of the OGL object. Otherwise, it will be the ID
        (multi-same-name support from version 1.1). Everything is fixed
        later.

        @param Element[] xmlOglClasses : XMI 'GraphicClass' elements
        @param {id / srcName, OglObject} dicoOglObjects : OGL objects loaded
        @param {id / srcName, OglLink} dicoLink : OGL links loaded
        @param {id / srcName, id / srcName} fathers: Inheritance
        @param UmlFrame umlFrame : Where to draw
        @param int oldData : If old data (v1.0), 1 else 0
        @since 2.0
        @author Philippe Waelti <pwaelti@eivd.ch>
        """

        pyutClass = PyutClass()

        # adding name for this class
        className =  xmlOglClasses.getElementsByTagName \
            ("Foundation.Core.ModelElement.name")

        if(len(className) > 0):
            name = className[0].firstChild
            if(name.nodeType == name.TEXT_NODE) :
                pyutClass.setName(name.data)

            oglClass = OglClass(pyutClass, 50, 50)

            # adding methods for this class
            pyutClass.setMethods(self._getMethods(xmlOglClasses))

            # adding fields for this class
            pyutClass.setFields(self._getFields(xmlOglClasses))


            # for class id
            classId = xmlOglClasses.getAttribute("xmi.id");
            print "Class ID : "+classId

            # for all class whos are inerithance link
            for fathers in xmlOglClasses.getElementsByTagName \
                ("Foundation.Core.Generalization"):
                linkId = fathers.getAttribute("xmi.idref")
                print "Father : " + linkId
                if(not self.dicoFather.has_key(linkId)):
                    self.dicoFather[linkId]={}
                self.dicoFather[linkId][classId] = oglClass


            # for all class whos are link
            for links in xmlOglClasses.getElementsByTagName \
                ("Foundation.Core.Classifier.associationEnd"):
                for link in links.getElementsByTagName("Foundation.Core.AssociationEnd"):
                    linkId = link.getAttribute("xmi.idref")
                    print  "LINK  " + linkId 
                    if(not self.dicoLinks.has_key(linkId)):
                        self.dicoLinks[linkId]=oglClass
                    #self.dicoLinks[linkId][classId] = oglClass


            dicoOglObjects[pyutClass.getId()] = oglClass


            umlFrame.addShape(oglClass, 100, 100)


    def open(self, dom, umlFrame):
        """
        To open a file and creating diagram.

        @since 1.0
        @Deve Roux <droux@eivd.ch>
        """
        from xml.dom.minidom import parse
        dicoOglObjects = {}  # format {name : oglClass}
        oldData = 0 # 1 if PyUT v1.0 files
        self.dicoLinks = {}   # format [name : PyutLink}
        self.dicoFather = {} # format {child oglClass : [fathers names]}
        self.dicoType = {}
        self.dicoReturn = {}


        # Load OGL Classes
        for Class in dom.getElementsByTagName("Foundation.Core.Class"):
           self._getOglClasses(Class, dicoOglObjects, umlFrame, oldData)

        # making link with xmi idType and method return and field
        self._getType(dom)
        
        self._getFathers(dom, umlFrame)
        self._getLinks(dom, umlFrame)

            
        # to draw diagram
        umlFrame.Refresh()

        # cleaning dico
        self.dicoType.clear()
        self.dicoReturn.clear()
        self.dicoFather.clear()
        self.dicoLinks.clear()

def main():
    #from xml.dom.minidom import parse
    filename="model.xml"
    dom = parse(StringIO(open(filename).read())) 

    myXmi = PyutXmi()
    myXmi.open(dom)


if __name__ == "__main__":
    main()
