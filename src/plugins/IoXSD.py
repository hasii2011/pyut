#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PyutType        import *
from PyutConsts      import *



# reading file
from StringIO import StringIO

from UmlFrame import *
from OglClass import OglClass
from OglLink  import *

from StringIO import StringIO
from PyutIoPlugin import PyutIoPlugin
import wx


class IoXSD(PyutIoPlugin):
    """
    To save XML file format.

    @version $Revision: 1.4 $
    """
    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @since 1.2
        """
        return "IoXSD"



    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "C.Dutoit <dutoitc@hotmail.com>"



    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @since 1.2
        """
        return "1.0"



    def getInputFormat(self):
        """
        Return a specification tupple.

        @return tupple
        @since 1.2
        """
        # return None if this plugin can't read.
        # otherwise, return a tupple with
        # - name of the input format
        # - extension of the input format
        # - textual description of the plugin input format
        # example : return ("Text", "txt", "Tabbed text...")
        return ("XSD", "xsd", "W3C XSD 1.0 file format?")



    def getOutputFormat(self):
        """
        Return a specification tupple.

        @return tupple
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        # return None if this plugin can't write.
        # otherwise, return a tupple with
        # - name of the output format
        # - extension of the output format
        # - textual description of the plugin output format
        # example : return ("Text", "txt", "Tabbed text...")
        #return ("XMI", "xml", "Pyut XMI file")
        return None



    def setExportOptions(self):
        """
        Prepare the export.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the export will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        #rep = wx.MessageBox("Do you want pretty xml ?", "Export option",
            #style = wx.YES_NO | wx.CANCEL | wx.CENTRE | wx.ICON_QUESTION)
        #self.pretty = (rep == wx.YES)
        #return rep != wx.CANCEL
        return False



    def write(self, oglObjects):
        """
        Write data to filename. Abstract.

        @return True if succeeded, False if error or canceled
        @param OglClass and OglLink [] : list of exported objects
        @author Deve Roux <droux@eivd.ch>
        @since 1.0
        """
        # Ask the user which destination file he wants
        #filename=self._askForFileExport()
        #if filename=="":
            #return False
        #file=open(filename, "w")
        return False

        


    #>------------------------------------------------------------------------


    def read(self, oglObjects, umlFrame):
        """
        Read data from filename. Abstract.

        @return True if succeeded, False if error or canceled
        @param OglClass and OglLink [] : list of imported objects
        @param UmlFrame : Pyut's UmlFrame
        @author Deve Roux <droux@eivd.ch>
        @since 1.0
        """
        #from xml.dom.minidom import parse
        
        # Ask the user which destination file he wants
        filename=self._askForFileImport()
        if filename=="":
            return False

        #dom = parse(StringIO(open(filename).read())) 

        return XSDReader(filename, umlFrame).process()


##############################################################################
##############################################################################
##############################################################################
from xml.dom.minidom import parse

class XSDReader:


    #>------------------------------------------------------------------------

    def __init__(self, filename, umlFrame):
        """
        Constructor
        """
        self._dom = parse(filename)
        self._umlFrame = umlFrame
        self._allElements = {}
        self._allAttGroups = {}
        self._refElements = []

        # Read namespace
        self._ns = self._readNamespace()


    #>------------------------------------------------------------------------

    def _readNamespace(self):
        """
        Read namespace
        """
        for attname, attvalue in self._dom.firstChild.attributes.items():
            if attvalue=="http://www.w3.org/2001/XMLSchema":
                return attname.split(":")[1]
        raise "Not found xmlns for XMLSchema"


    #>------------------------------------------------------------------------

    def process(self):
        """
        Process
        """
        # Read all elements first
        for node in self._dom.firstChild.childNodes:
            if node.nodeName==self._ns + ":element":
                self._readElementOnly(node)
            elif node.nodeName==self._ns + ":attributeGroup":
                self._readAttributeGroupOnly(node)
            elif node.nodeName==self._ns + ":simpleType":
                self._readSimpleType(node)
            elif node.nodeName==self._ns + ":complexType":
                pass
            elif node.nodeName==self._ns + "annotation":
                pass
            elif node.nodeName[0]=="#":
                pass
            else:
                print "Ignored /", node.nodeName

        doc = self._getDoc(self._dom.firstChild)
        if len(doc.strip())>0:
            note = self._umlFrame.createNewNote(0, 0)
            note.setName(doc)


        # Read all elements type
        for context in self._allElements.values():
            for child in context.node.childNodes:
                if child.nodeName==self._ns + ":complexType":
                    self._readComplexType(context, child)
                elif child.nodeName==self._ns + ":annotation":
                    pass # Already handled in readElementOnly
                elif child.nodeName[0]=="#":
                    pass
                else:
                    print "Ignored tag:" + child.nodeName


    #>------------------------------------------------------------------------

    def _getDoc(self, node):
        """
        read .//xs:annotation//xs:documentation tags
        """
        doc=""
        l1 = [el for el in node.childNodes 
              if el.nodeName in ["xsd:annotation", "xs:annotation"]]
        for n1 in l1: 
            l2 = [el for el in l1[0].childNodes 
                  if el.nodeName in ["xsd:documentation", "xs:documentation"]]
            for n2 in l2:
                if (n2.firstChild.nodeValue==None):
                    print "getDoc got an empty node !"
                else:
                    doc+=n2.firstChild.nodeValue.replace("\n", " ")
        return doc


    #>------------------------------------------------------------------------

    def _createClass(self, name, x, y):
        """
        Create a class (pyutClass and oglClass)
        @return pyutClass, oglClass
        """
        pyutClass = PyutClass()
        pyutClass.setName(name)
        oglClass = OglClass(pyutClass, 50, 50)
        self._umlFrame.addShape(oglClass, x, y)
        return pyutClass, oglClass


    #>------------------------------------------------------------------------

    def _readElementOnly(self, node):
        """
        Read xsd:element
        """
        # Read name, type
        name = node.getAttribute("name")
        #type = node.getAttribute("type")

        # Save
        pc, oc = self._createClass(name, 0, 0)
        self._allElements[name] = Context(node, name, pc, oc)

        # Read annotation/documentation
        doc = self._getDoc(node)
        pc.setDescription(doc)


    #>------------------------------------------------------------------------

    def _readSimpleType(self, node):
        doc = self._getDoc(node)
        for child in node.childNodes:
            if child.nodeName[0]=="#":
                pass
            elif child.nodeName==self._ns + ":restriction":
                lstPatterns = [el for el in child.childNodes 
                        if el.nodeName==self._ns + ":pattern"]
                if len(lstPatterns)==1:
                    pattern = lstPatterns[0].getAttribute("value")     
                    doc+="" + pattern
                else:
                    print "Ignored xs:pattern"
                
            else:
                print "Ignored SimpleType/", child.nodeName
        if len(doc.strip())>0:
            note = self._umlFrame.createNewNote(0, 0)
            note.setName(doc)



    #>------------------------------------------------------------------------

    def _readAttributeGroupOnly(self, node):
        """
        Read xsd:attributeGroup
        """
        # Read name, type
        name = node.getAttribute("name")

        # Save
        #pc, oc = self._createClass(name, 0, 0)
        self._allAttGroups[name] = Context(node, name, None, None)

        # Read annotation/documentation
        #doc = self._getDoc(node)
        #pc.setDescription(doc)


    #>------------------------------------------------------------------------

    def _completeElement(self, node):
        """
        Read xs:element/
        """



#
#
#    #>------------------------------------------------------------------------
#
#    def _readElement(self, node):
#        """
#        Read xsd:element
#        """
#        # Read name, type
#        name = node.getAttribute("name")
#        type = node.getAttribute("type")
#
#        # Save
#        pc, oc = self._createClass(name, 0, 0)
#        self._allElements.append(Context(node, name, pc, oc))
#
#        # Read annotation/documentation
#        doc = self._getDoc(node)
#        pc.setDescription(doc)
#        
#        # Read xsd:sequence
#        for node in node.childNodes:
#            if node.nodeName in ["xsd:sequence", "xs:sequence"]:
#                self._readSequence(node, pc, oc)
#            elif node.nodeName in ["xsd:attribute", "xs:attribute"]:
#                self._readAttribute(node, pc, oc)
#            elif node.nodeName in ["xsd:annotation", "xs:annotation"]:
#                pass #Already readed
#            elif node.nodeName in ["xsd:complexType", "xs:complexType"]:
#                #print "Unsupported tag(1): ", node.nodeName
#                self._readComplexType(node, pc, oc)
#            elif node.nodeName=="#text":
#                pass
#            elif node.nodeName=="#comment":
#                pass
#            else:
#                print "Unread tag(1):" + node.nodeName
#                    
#
#
#        return pc, oc
#

    #>------------------------------------------------------------------------

    def _readSequence(self, context, node):
        """
        Read xsd:sequence
        """
        # Read xsd:element and do recursion
        for child in node.childNodes:
            if child.nodeName == self._ns + ":element":
                ref = child.getAttribute("ref")
                if self._allElements.has_key(ref):
                    context2 = self._allElements[ref]
                    vmin = child.getAttribute("minOccurs")
                    vmax = child.getAttribute("maxOccurs")
                    if vmax=="unbounded":vmax="n"

                    # Do link
                    link = self._umlFrame.createNewLink(context.oc, 
                            context2.oc, OGL_AGGREGATION)
                    link.getPyutObject().setSrcCard(vmin + ".." + vmax)
                else:
                    print "Key not found for xs:sequence[@ref=",ref,"]"
            #elif node.nodeName in ["xsd:sequence", "xs:sequence"]:
                #self._readSequence(context)
            elif child.nodeName[0]=="#":
                pass
            else:
                print "Unread tag(2):" + child.nodeName


    #>------------------------------------------------------------------------

    def _readComplexType(self, context, node):
        """
        Read xsd:complexType
        """

        # Children
        for child in node.childNodes:
            if child.nodeName == self._ns + ":sequence":
                self._readSequence(context, child)
            elif child.nodeName == self._ns + ":attribute":
                self._readAttribute(context, child)
            #elif node.nodeName in ["xsd:annotation", "xs:annotation"]:
                #doc = self._getDoc(node)
                #pc.setDescription(doc)
            elif child.nodeName == self._ns + ":attributeGroup":
                self._readAttributeGroup(child, context)
            elif child.nodeName=="#text":
                pass
            elif child.nodeName=="#comment":
                pass
            else:
                print "Unread tag(3):" + child.nodeName


    #>------------------------------------------------------------------------

    def _readAttribute(self, context, node):
        """
        Read xsd:attribute
        """
        field = PyutField()
        field.setName(node.getAttribute("name"))
        field.setType(PyutType(node.getAttribute("type") + 
                " (" + node.getAttribute("use") + ")"))
        value = node.getAttribute("fixed")
        if (value!=None and value!=""):
            field.setDefaultValue(node.getAttribute("fixed"))
        context.pc.addField(field)

    #>------------------------------------------------------------------------

    def _readAttributeGroup(self, node, parentContext):
        """
        read xsd:attributeGroup
        """
        ref = node.getAttribute("ref")
        context = self._allAttGroups[ref]
        
        for child in context.node.childNodes:
            if child.nodeName == self._ns + ":attribute":
                name = child.getAttribute("name")
                type = child.getAttribute("type")
                use  = child.getAttribute("use")

                field = PyutField()
                field.setName(name)
                field.setType(PyutType(str(type) + " " + str(use)))
                # TODO : support documentation in PyUt for Attributes
                #if (attDef!="None"): 
                    #field.setDefaultValue(attDef)
                parentContext.pc.addField(field)
            elif child.nodeName[0]=="#":
                pass
            else:
                print "Unsupported tag: attributeGroup/", child.nodeName



#
#
#    def _old(self):
#        #print "-------------------- attribute ---------------"
#        #print self._attribute
#
#        # elementType sample :
#        #{u'GraphicClass': ('',   [(u'Class',         '')  ], ''), 
#        # u'GraphicNote':  ('',   [(u'Note',          '')  ], ''), 
#        # u'LabelCenter':  ('',   [( '#PCDATA',       '')  ], ''), 
#        # u'LabelDst':     ('',   [( '#PCDATA',       '')  ], ''), 
#        # u'Note':         ('',   [( '#PCDATA',       '')  ], ''), 
#        # u'PyutDocument': (u'|', [(u'GraphicClass', u'*'), 
#        #                          (u'GraphicNote',  u'*'), 
#        #                          (u'GraphicLink',  u'*') ], ''), 
#        # u'PyutProject':  ('',   [(u'PyutDocument', u'*') ], ''), 
#        # u'LabelSrc':     ('',   [('#PCDATA',        '')  ], ''), 
#        # u'Link':         ('',   [('#PCDATA',        '')  ], ''), 
#        # u'Class':        ('',   [('#PCDATA',        '')  ], ''), 
#        # u'GraphicLink':  (u',', [(u'LabelCenter',   ''), 
#        #                          (u'LabelSrc',      ''), 
#        #                          (u'LabelDst',      ''), 
#        #                          (u'Link',          '')  ], '')}
#
#
#        # Import elements as classes
#        elementsTree = {}       # pyutClass, oglClass, lstChildrenElementName
#        x=50
#        y=50
#        for element in self._elementType.keys():
#            pyutClass, oglClass = self._createClass(element, x, y)
#            elementsTree[element] = (pyutClass, oglClass, [])
#
#            # Graphic care
#            if x<800: 
#                x+=80
#            else:
#                x=80
#                y+=80
#
#        # Import links
#        for element in elementsTree.keys():
#            parent_pyutClass, parent_oglClass, dummy = elementsTree[element]
#
#            if self._elementType[element]=="EMPTY":
#                pass
#            else:
#                sep, cont, mod = self._elementType[element]
#                #TODO : handle sep and mod
#                for tuple in cont:
#                    # Note : ANY->NONE, EMPTY->("", [], "")
#                    if len(tuple)==2:
#                        name, mod = tuple
#                        if not elementsTree.has_key(name):
#                            pyutClass, oglClass = self._createClass(name, 100, 200)
#                            elementsTree[name] = (pyutClass, oglClass, [])
#                        childOglClass = elementsTree[name][1]
#
#
#                        # Get cardinality
#                        cardinality=""
#                        if mod in ['*', '+', '?']: cardinality = mod
#
#                        # Create link
#                        link = self._umlFrame.createNewLink(parent_oglClass, 
#                                                            childOglClass,
#                                        OGL_AGGREGATION)
#                        pyutLink = link.getPyutObject()
#                        pyutLink.setDestCard(cardinality)
#                    elif len(tuple)==3:
#                        sep, cont, mod = tuple
#                        # TODO : handle this
#                    else:
#                        raise "Unsupported exception"
#
#        # TODO : self._elementType.keys not in self._elementsTree.keys
#                
#
#
#
#        # Import attributes
#        for parentElement in self._attribute.keys():
#            # test
#            if not elementsTree.has_key(parentElement):
#                displayError(_("Wrong DTD : An attribute refers to " + 
#                    elementName + ", but this is element is not declared."))
#            else:
#                # Get parent elements
#                pyutClass = elementsTree[parentElement][0]
#                #oglClass  = elementsTree[elementName][1]
#
#                # Read all attributes for the parent
#                for attributesTuple in self._attribute[parentElement]:
#                    attName, attType, attDecl, attDef = attributesTuple
#
#                    # Create field
#                    field = PyutField()
#                    field.setName(attName)
#                    field.setType(PyutType(str(attType) + " " + str(attDecl)))
#                    if (attDef!="None" and attDef!=None): 
#                        field.setDefaultValue(attDef)
#                    pyutClass.addField(field)
#        
#
#        #'elem' is the name of the element, 'attr' the name of the attribute, 
#        #'a_type' the name of the attribute type (ID, CDATA...), 
#        #'a_decl' the name of the declared default type (#REQUIRED, #IMPLIED...)
#        #and 'a_def' the declared default value (or None if none were declared). 
            




##############################################################################
##############################################################################
##############################################################################

class Context:
    def __init__(self, node, name, pc, oc):
        self.node = node
        self.name = name
        self.pc = pc
        self.oc = oc
