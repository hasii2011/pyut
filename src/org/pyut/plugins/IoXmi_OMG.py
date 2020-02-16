
from logging import Logger
from logging import getLogger

from xml.dom.minidom import parse

from io import StringIO

import wx

from org.pyut.ogl.OglClass import OglClass

from org.pyut.PyutUtils import PyutUtils

from org.pyut.model.PyutField import PyutField
from org.pyut.PyutClass import PyutClass
from org.pyut.PyutLink import PyutLink

from org.pyut.plugins.PyutIoPlugin import PyutIoPlugin


class IoXmi_OMG(PyutIoPlugin):
    """
    XMI import plugin

    Plugin call
    -----------
    To use a plugin :
     - plg = IoXmi_OMG(...)
     - plg.doImport()
     - plg.doExport()


    @author C.Dutoit <dutoitc@hotmail.com>
    @version $Revision: 1.5 $
    """
    def __init__(self, oglObjects, umlFrame):
        """
        Constructor.

        @param OglObject oglObjects : list of ogl objects
        @param UmlFrame umlFrame : the umlframe of pyut
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        super().__init__(oglObjects, umlFrame)

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author C.Dutoit
        """
        return "IoXmi_OMG"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @author C.Dutoit
        """
        return "C.Dutoit <dutoitc@hotmail.com>"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @author C.Dutoit
        """
        return "1.0a"

    def getInputFormat(self):
        """
        Return a specification tupple.

        @return tuple
        @author C.Dutoit
        """
        return "XMI-OMG 1.1", "xmi", "XMI 1.1 from OMG specifications"

    def read(self, oglObjects, umlFrame):
        """
        Read data from filename

        @param oglObjects  list of imported objects
        @param umlFrame : Pyut's UmlFrame
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        wx.BeginBusyCursor()
        filename = self._askForFileImport()
        importer = XmiImporter(filename, umlFrame)
        importer.doImport()
        wx.EndBusyCursor()


class XmiImporter:
    """
    import XMI file from OMG 1.1 XMI specifications

    Common use :
    ============
    importer = XmiImporter(filename, umlFrame)
    importer.doImport()

    @author C.Dutoit <dutoitc@hotmail.com>
    """
    def __init__(self, filename, umlFrame):
        """
        Constructor
        @param filename : filename to import datas from
        @param umlFrame : frame to which add uml objects
        @author C.Dutoit
        """
        self.logger: Logger = getLogger(__name__)

        # Read file and init

        self._dom = parse(StringIO(open(filename).read()))
        self._umlFrame = umlFrame

        # Init class fields
        self.dicOglClasses = {}
        self._dicOglClasses = {}  # Dictionary of {XMI.ID:OglClass}

    def doImport(self):
        """
        Import datas from file to uml frame
        @author C.Dutoit
        """
        # Read XMI
        xmi = self._dom.getElementsByTagName("XMI")
        if len(xmi) == 0:

            PyutUtils.displayError("Wrong XMI File format : XMI tag not found !")
            return
        else:
            xmi = xmi[0]

        # Read XMI.header
        self._readXMIHeader(xmi)

        # Read XMI content
        self._readXMIContent(xmi)

    def _readXMIHeader(self, xmi):
        """
        Read XMI/XMI.header
        @param xmi : XMI element
        @author C.Dutoit
        """
        # Get XMI.header
        xmi_header = xmi.getElementsByTagName("XMI.header")
        if len(xmi_header) == 0:
            return
        xmi_header = xmi_header[0]

        # Read documentation
        self._readXMIDocumentation(xmi_header)

    def _readXMIDocumentation(self, xmi_header):
        """
        Read XMI/XMI.documentation
        @param xmi_header : XMI.header element
        @author C.Dutoit
        """
        # Get XMI.documentation
        xmi_documentation = xmi_header.getElementsByTagName("XMI.documentation")
        if len(xmi_documentation) == 0:
            return
        xmi_documentation = xmi_documentation[0]

        # Set documentation dictionary
        dic = {"XMI.owner": "Owner",
               "XMI.contact": "Contact",
               "XMI.longDescription": "Long description",
               "XMI.shortDescription": "Short description",
               "XMI.exporter": "Exporter",
               "XMI.exporterVersion": "Exporter version",
               "XMI.notice": "Notice"}

        for tag in list(dic.keys()):
            tag_content = xmi_documentation.getElementsByTagName(tag)
            if len(tag_content) > 0:
                self.logger.info(tag + " : ", end=' ')
                self.logger.info(tag_content[0].firstChild.wholeText)
                # print tag_content[0].firstChild.data

    def _readXMIContent(self, xmi):
        """
        Read XMI/XMI.content
        @param xmi : XMI element
        @author C.Dutoit
        """
        # Get XMI.header
        xmi_content = xmi.getElementsByTagName("XMI.content")
        if len(xmi_content) == 0:
            return
        xmi_content = xmi_content[0]

        # Read classes
        self._readAllFoundationCoreClass(xmi_content)

        # Read associations
        self._readAllFoundationCoreAssociation(xmi_content)

        # Read abstractions
        self._readAllFoundationCoreAbstraction(xmi_content)

    def _readAllFoundationCoreClass(self, xmiContent):
        """
        Read all Foundation.Core.Class
        @param xmiContent : XMI.content element
        @author C.Dutoit
        """
        # Get classes
        for xmiClass in xmiContent.getElementsByTagName("Foundation.Core.Class"):
            self._readFoundationCoreClass(xmiClass)

    def _readFoundationCoreClass(self, coreClass):
        """
        Read one Foundation.Core.Class
        @param coreClass : Foundation.Core.Class element
        @author C.Dutoit
        """
        # Get class name
        className = self._readFoundationCoreClassName(coreClass)
        self.logger.info("Reading class ", className, end=' ')

        # Get class ID
        classID = str(coreClass.getAttribute("xmi.id"))
        self.logger.info("id = ", classID, end=' ')

        # Save class
        pyutClass = PyutClass(className)

        # Get class abstract status
        isAbstract = self._readFoundationCoreClassIsAbstract(coreClass)
        self.logger.info("isAbstract = ", isAbstract)
        if isAbstract:
            pyutClass.setStereotype("Abstract")

        # Get class features
        self._readFoundationCoreClassifierFeature(coreClass, pyutClass)

        # Make the PyutClass visible
        oglClass = OglClass(pyutClass)
        x = (len(self._dicOglClasses) % 10) * 100
        y = len(self._dicOglClasses) / 10 * 100
        self._umlFrame.addShape(oglClass, x, y)
        oglClass.autoResize()
        self._dicOglClasses[classID] = oglClass

    def _readFoundationCoreClassName(self, coreClass):
        """
        Read one Foundation.Core.Class
        @param coreClass : Foundation.Core.Class element
        @return class name
        @author C.Dutoit
        """
        xmiName = coreClass.getElementsByTagName("Foundation.Core.ModelElement.name")
        if len(xmiName) > 0:
            return xmiName[0].firstChild.wholeText
        else:
            return "Unnamed class"

    def _readFoundationCoreClassIsAbstract(self, coreClass):
        """
        Read one Foundation.Core.Class
        @param coreClass : Foundation.Core.Class element
        @return 1/0 if the class is abstract or not
        @author C.Dutoit
        """
        # Get class abstract status
        xmiIsAbstract = coreClass.getElementsByTagName("Foundation.Core.GeneralizableElement.isAbstract")
        if len(xmiIsAbstract) > 0:
            return xmiIsAbstract[0].getAttribute("xmi.value") == "True"
        else:
            return 0

    def _readFoundationCoreClassifierFeature(self, coreClass, pyutClass):
        """
        Read one Foundation.Core.Class
        @param coreClass : Foundation.Core.Class element
        @param pyutClass  : PyutClass object to which add features
        @return 1/0 if the class is abstract or not
        @author C.Dutoit
        """
        # Get feature
        xmiFeature = coreClass.getElementsByTagName("Foundation.Core.Classifier.feature")
        if len(xmiFeature) == 0:
            return

        # Read all feature attribute
        pyutFields = []
        for xmiAttribute in xmiFeature[0].getElementsByTagName("Foundation.Core.Attribute"):
            self.logger.info("Attribute ", end=' ')

            # Read attribute name
            el = xmiAttribute.getElementsByTagName("Foundation.Core.ModelElement.name")
            if len(el) > 0:
                name = el[0].firstChild.wholeText
            else:
                name = "Unnamed_Attribute"
            self.logger.info(name, end=' ')

            # Read attribute visibility
            el = xmiAttribute.getElementsByTagName("Foundation.Core.ModelElement.visibility")
            if len(el) > 0:
                visibility = el[0].getAttribute("xmi.value")
            else:
                visibility = "Unvisibilityd_Attribute"
            self.logger.info("v=", visibility)

            # Add feature attribute to pyut Fields
            # name, type, def, vis
            pyutFields.append(PyutField(name, "", None, visibility))

        # Add feature attributes to pyutClass
        pyutClass.setFields(pyutFields)

    def _readAllFoundationCoreAssociation(self, xmiContent):
        """
        Read all Foundation.Core.Association
        @param xmiContent : XMI.content element
        @author C.Dutoit
        """
        # Get classes
        for xmiAssociation in xmiContent.getElementsByTagName("Foundation.Core.Association"):
            self._readFoundationCoreAssociation(xmiAssociation)

    def _readFoundationCoreAssociation(self, xmiAssociation):
        """
        Read one Foundation.Core.Association
        @param xmiAssociation : association to be read
        @author C.Dutoit
        """
        # Get connection element
        conn = xmiAssociation.getElementsByTagName(
                                    "Foundation.Core.Association.connection")
        if len(conn) != 1:
            return
        conn = conn[0]

        # Get the two associations end
        ends = conn.getElementsByTagName("Foundation.Core.AssociationEnd")
        if len(ends) != 2:
            self.logger.error("Invalid association : needed 2 ends, got ", len(ends))
            return

        # Read associations end type
        endsValues = []
        for i in range(2):
            endType = ends[i].getElementsByTagName("Foundation.Core.AssociationEnd.type")
            if len(endType) != 1:
                self.logger.error("Invalid association end type")
                return
            endType = endType[0]

            # Read association end type classifier
            classifier = endType.getElementsByTagName("Foundation.Core.Classifier")
            if len(classifier) != 1:
                self.logger.error("Invalid association end type classifier")
                return
            classifier = classifier[0]
            xmi_id = str(classifier.getAttribute("xmi.idref"))

            # Read association end multiplicity
            multiplicity = ends[i].getElementsByTagName("Foundation.Core.AssociationEnd.multiplicity")
            if len(multiplicity) > 0:
                multiplicity = multiplicity[0].firstChild.wholeText
            else:
                multiplicity = ""

            # Read association type
            isAggregation = ends[i].getElementsByTagName("Foundation.Core.AssociationEnd.aggregation")
            if len(isAggregation) > 0:
                self.logger.info(isAggregation[0])
                self.logger.info(isAggregation[0].firstChild)
                isAggregation = isAggregation[0].getElementsByTagName("xmi.value") != "none"
            else:
                isAggregation = False

            # Save end
            endsValues.append((xmi_id, multiplicity, isAggregation))

        # Create link
        if endsValues[0][0] in self._dicOglClasses and endsValues[1][0] in self._dicOglClasses:
            # Get classes
            srcOgl = self._dicOglClasses[endsValues[0][0]]
            dstOgl = self._dicOglClasses[endsValues[1][0]]

            # Create link
            if endsValues[0][2]:
                oglLink = self._umlFrame.createNewLink(srcOgl, dstOgl)
            elif endsValues[1][2]:
                oglLink = self._umlFrame.createNewLink(dstOgl, srcOgl)
            else:
                oglLink = self._umlFrame.createNewLink(srcOgl, dstOgl)

            # Add parameters
            pyutLink: PyutLink = oglLink.getPyutObject()
            # pyutLink.setSourceCardinality(endsValues[0][1])
            # pyutLink.setDestinationCardinality(endsValues[1][1])
            pyutLink.sourceCardinality      = endsValues[0][1]
            pyutLink.destinationCardinality = endsValues[1][1]

    def _readAllFoundationCoreAbstraction(self, xmiContent):
        """
        Read all Foundation.Core.Abstraction
        @param xmiContent : XMI.content element
        @author C.Dutoit
        """
        # Get classes
        for xmiAbstraction in xmiContent.getElementsByTagName(
                                              "Foundation.Core.Abstraction"):
            self._readFoundationCoreAbstraction(xmiAbstraction)

    def _readFoundationCoreAbstraction(self, xmiAbstraction):
        """
        Read one Foundation.Core.Abstraction
        @param xmiAbstraction : association to be read
        @author C.Dutoit
        """
        # Get client
        client = xmiAbstraction.getElementsByTagName("Foundation.Core.Dependency.client")
        if len(client) == 0:
            self.logger.error("Error : Foundation.Core.Dependency.client not found !")
            return

        # Get model element
        modelElement = client[0].getElementsByTagName("Foundation.Core.ModelElement")
        if len(modelElement) == 0:
            self.logger.error("Error : Foundation.Core.Dependency.Client has no elements ", end=' ')
            self.logger.error("Foundation.Core.ModelElements !")
            return
        # clientID = str(modelElement[0].getAttribute("xmi.idref"))

        # Get supplier
        supplier = xmiAbstraction.getElementsByTagName("Foundation.Core.Dependency.supplier")
        if len(supplier) == 0:
            self.logger.error("Error : Foundation.Core.supplier not found !")
            return

        # Get model element
        modelElement = supplier[0].getElementsByTagName("Foundation.Core.ModelElement")
        if len(modelElement) == 0:
            self.logger.error("Error : Foundation.Core.Dependency.supplier has no elements ", end=' ')
            self.logger.error("Foundation.Core.ModelElements !")
            return
        # supplierID = str(modelElement[0].getAttribute("xmi.idref"))

        # Get classes
        # srcOgl = self._dicOglClasses[clientID]
        # dstOgl = self._dicOglClasses[supplierID]
