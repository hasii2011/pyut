
from logging import Logger
from logging import getLogger

from xml.dom.minidom import parse

from org.pyut.plugins.PyutIoPlugin import PyutIoPlugin

from org.pyut.PyutClass import PyutClass
from org.pyut.PyutType import PyutType
from org.pyut.PyutField import PyutField

from org.pyut.enums.OglLinkType import OglLinkType

from org.pyut.ogl.OglClass import OglClass


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
        return "XSD", "xsd", "W3C XSD 1.0 file format?"

    def getOutputFormat(self):
        """
        Return a specification tupple.

        @return tupple
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return None

    def setExportOptions(self):
        """
        Prepare the export.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the export will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        return False

    def write(self, oglObjects):
        """
        Write data to filename. Abstract.

        @return True if succeeded, False if error or canceled
        @param oglObjects list of exported objects
        @author Deve Roux <droux@eivd.ch>
        @since 1.0
        """
        return False

    def read(self, oglObjects, umlFrame):
        """
        Read data from filename. Abstract.

        @return True if succeeded, False if error or canceled
        @param oglObjects : list of imported objects
        @param umlFrame : Pyut's UmlFrame
        @author Deve Roux <droux@eivd.ch>
        @since 1.0
        """
        # from xml.dom.minidom import parse

        # Ask the user which destination file he wants
        filename = self._askForFileImport()
        if filename == "":
            return False

        # dom = parse(StringIO(open(filename).read()))

        return XSDReader(filename, umlFrame).process()


class XSDReader:

    def __init__(self, filename, umlFrame):
        """
        Constructor
        """
        self.logger: Logger = getLogger(__name__)
        self._dom = parse(filename)
        self._umlFrame = umlFrame
        self._allElements = {}
        self._allAttGroups = {}
        self._refElements = []

        # Read namespace
        self._ns = self._readNamespace()

    def _readNamespace(self):
        """
        Read namespace
        """
        for attname, attvalue in list(self._dom.firstChild.attributes.items()):
            if attvalue == "http://www.w3.org/2001/XMLSchema":
                return attname.split(":")[1]
        raise Exception("Not found xmlns for XMLSchema")

    def process(self):
        """
        Process
        """
        # Read all elements first
        for node in self._dom.firstChild.childNodes:
            if node.nodeName == self._ns + ":element":
                self._readElementOnly(node)
            elif node.nodeName == self._ns + ":attributeGroup":
                self._readAttributeGroupOnly(node)
            elif node.nodeName == self._ns + ":simpleType":
                self._readSimpleType(node)
            elif node.nodeName == self._ns + ":complexType":
                pass
            elif node.nodeName == self._ns + "annotation":
                pass
            elif node.nodeName[0] == "#":
                pass
            else:
                self.logger.warning(f"Ignored: {node.nodeName}")

        doc = self._getDoc(self._dom.firstChild)
        if len(doc.strip()) > 0:
            note = self._umlFrame.createNewNote(0, 0)
            note.setName(doc)

        # Read all elements type
        for context in list(self._allElements.values()):
            for child in context.node.childNodes:
                if child.nodeName == self._ns + ":complexType":
                    self._readComplexType(context, child)
                elif child.nodeName == self._ns + ":annotation":
                    pass  # Already handled in readElementOnly
                elif child.nodeName[0] == "#":
                    pass
                else:
                    self.logger.warning(f"Ignored tag: {child.nodeName}")

    def _getDoc(self, node):
        """
        read .//xs:annotation//xs:documentation tags
        """
        doc = ""
        l1 = [el for el in node.childNodes
              if el.nodeName in ["xsd:annotation", "xs:annotation"]]

        # noinspection PyUnusedLocal
        for n1 in l1:
            l2 = [el for el in l1[0].childNodes
                  if el.nodeName in ["xsd:documentation", "xs:documentation"]]
            for n2 in l2:
                if n2.firstChild.nodeValue is None:
                    self.logger.warning("getDoc got an empty node !")
                else:
                    doc += n2.firstChild.nodeValue.replace("\n", " ")
        return doc

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

    def _readElementOnly(self, node):
        """
        Read xsd:element
        """
        # Read name, type
        name = node.getAttribute("name")
        # type = node.getAttribute("type")

        # Save
        pc, oc = self._createClass(name, 0, 0)
        self._allElements[name] = Context(node, name, pc, oc)

        # Read annotation/documentation
        doc = self._getDoc(node)
        pc.setDescription(doc)

    def _readSimpleType(self, node):
        doc = self._getDoc(node)
        for child in node.childNodes:
            if child.nodeName[0] == "#":
                pass
            elif child.nodeName == self._ns + ":restriction":
                lstPatterns = [el for el in child.childNodes if el.nodeName == self._ns + ":pattern"]
                if len(lstPatterns) == 1:
                    pattern = lstPatterns[0].getAttribute("value")
                    doc += "" + pattern
                else:
                    self.logger.warning("Ignored xs:pattern")

            else:
                self.logger.warning("Ignored SimpleType/", child.nodeName)
        if len(doc.strip()) > 0:
            note = self._umlFrame.createNewNote(0, 0)
            note.setName(doc)

    def _readAttributeGroupOnly(self, node):
        """
        Read xsd:attributeGroup
        """
        # Read name, type
        name = node.getAttribute("name")
        self._allAttGroups[name] = Context(node, name, None, None)

    def _completeElement(self, node):
        """
        Read xs:element/
        """
        pass    # hasii There was no code here

    def _readSequence(self, context, node):
        """
        Read xsd:sequence
        """
        # Read xsd:element and do recursion
        for child in node.childNodes:
            if child.nodeName == self._ns + ":element":
                ref = child.getAttribute("ref")
                if ref in self._allElements:
                    context2 = self._allElements[ref]
                    vmin = child.getAttribute("minOccurs")
                    vmax = child.getAttribute("maxOccurs")
                    if vmax == "unbounded":
                        vmax = "n"

                    # Do link
                    link = self._umlFrame.createNewLink(context.oc, context2.oc, OglLinkType.OGL_AGGREGATION)
                    link.getPyutObject().setSrcCard(vmin + ".." + vmax)
                else:
                    self.logger.warning(f"Key not found for xs:sequence[@ref={ref}]")
            elif child.nodeName[0] == "#":
                pass
            else:
                self.logger.warning(("Unread tag(2):" + child.nodeName))

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
            elif child.nodeName == self._ns + ":attributeGroup":
                self._readAttributeGroup(child, context)
            elif child.nodeName == "#text":
                pass
            elif child.nodeName == "#comment":
                pass
            else:
                self.logger.warning(f"Unread tag(3): {child.nodeName}")

    def _readAttribute(self, context, node):
        """
        Read xsd:attribute
        """
        field = PyutField()
        field.setName(node.getAttribute("name"))
        field.setType(PyutType(node.getAttribute("type") + " (" + node.getAttribute("use") + ")"))
        value = node.getAttribute("fixed")
        if value is None and value != "":
            field.setDefaultValue(node.getAttribute("fixed"))
        context.pc.addField(field)

    def _readAttributeGroup(self, node, parentContext):
        """
        read xsd:attributeGroup
        """
        ref = node.getAttribute("ref")
        context = self._allAttGroups[ref]

        for child in context.node.childNodes:
            if child.nodeName == self._ns + ":attribute":
                name = child.getAttribute("name")
                cType = child.getAttribute("type")
                use  = child.getAttribute("use")

                field = PyutField()
                field.setName(name)
                field.setType(PyutType(str(cType) + " " + str(use)))
                # TODO : support documentation in PyUt for Attributes
                # if (attDef!="None"):
                    # field.setDefaultValue(attDef)
                parentContext.pc.addField(field)
            elif child.nodeName[0] == "#":
                pass
            else:
                self.logger.warning("Unsupported tag: attributeGroup:  {child.nodeName}")


class Context:
    def __init__(self, node, name, pc, oc):
        self.node = node
        self.name = name
        self.pc = pc
        self.oc = oc
