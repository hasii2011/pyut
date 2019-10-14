
# TODO : ELEMENT x (#CDATA) -> ajouter un field #CDATA

from org.pyut.PyutType import *

# from xml.parsers.xmlproc.dtdparser import DTDParser, DTDConsumer  #  TODO have to figure out where to get this from

from org.pyut.ogl.OglClass import OglClass

from plugins.PyutIoPlugin import PyutIoPlugin

from globals import _


class IoDTD(PyutIoPlugin):
    """
    To save XML file format.

    @version $Revision: 1.8 $
    """
    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "IoDTD"

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
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        return "1.0"

    def getInputFormat(self):
        """
        Return a specification tupple.

        @return tupple
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.2
        """
        # return None if this plugin can't read.
        # otherwise, return a tupple with
        # - name of the input format
        # - extension of the input format
        # - textual description of the plugin input format
        # example : return ("Text", "txt", "Tabbed text...")
        return "DTD", "dtd", "W3C DTD 1.0 file format"

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
        @param oglObjects : list of exported objects
        @author Deve Roux <droux@eivd.ch>
        @since 1.0
        """
        return False

    def read(self, oglObjects, umlFrame):
        """
        Read data from filename. Abstract.

        @return True if succeeded, False if error or canceled
        @param oglObjects list of imported objects
        @param umlFrame : Pyut's UmlFrame
        @author Deve Roux <droux@eivd.ch>
        @since 1.0
        """
        # Ask the user which destination file he wants
        filename=self._askForFileImport()
        if filename == "":
            return False

        return DTDReader().open(filename, umlFrame)


# class DTDReader(DTDConsumer):
class DTDReader():

    def __init__(self):
        # self._parser = DTDParser()
        # DTDConsumer.__init__(self, self._parser)      # Where oh where will I get this?  hasii

        self._parser = None

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

    def open(self, filename, umlFrame):
        """
        Open DTD
        """
        # Init
        self._umlFrame = umlFrame
        self._attributes = {}
        self._externalEntity = {}
        self._generalEntity = {}
        self._parameterEntity = {}
        self._externalPe = {}
        self._notation = {}
        self._elementType = {}
        self._attribute = {}

        # Parse
        self._parser.set_dtd_consumer(self)
        self._parser.feed(open(filename, "r").read())
        self._parser.close()

        # Do best !
        for oglObject in self._umlFrame.getUmlObjects():
            try:
                oglObject.autoResize()
            except (ValueError, Exception) as e:
                print(f'Error: {e}')

    def set_error_handler(self, err):
        """
        Sets the error handler of the DTDConsumer.
        """
        pass

    def dtd_start(self):
        """
        Called before any DTD events arrive.
        (Note: This will be called once for the internal DTD subset (if any)
        and once for the external DTD subset (if parsed).)
        """
        pass

    def dtd_end(self):
        """
        Called when the DTD is completely parsed.
        (Note: This will be called once for the internal DTD subset (if any)
        and once for the external DTD subset (if parsed).)
        """
        elementsTree = {}       # pyutClass, oglClass, lstChildrenElementName
        x = 50
        y = 50
        for element in list(self._elementType.keys()):
            pyutClass, oglClass = self._createClass(element, x, y)
            elementsTree[element] = (pyutClass, oglClass, [])

            # Graphic care
            if x < 800:
                x += 80
            else:
                x = 80
                y += 80

        # Import links
        for element in list(elementsTree.keys()):
            parent_pyutClass, parent_oglClass, dummy = elementsTree[element]

            if self._elementType[element] == "EMPTY":
                pass
            else:
                sep, cont, mod = self._elementType[element]
                # TODO : handle sep and mod
                for tuple in cont:
                    # Note : ANY->NONE, EMPTY->("", [], "")
                    if len(tuple) == 2:
                        name, mod = tuple
                        if name not in elementsTree:
                            pyutClass, oglClass = self._createClass(name, 100, 200)
                            elementsTree[name] = (pyutClass, oglClass, [])
                        childOglClass = elementsTree[name][1]

                        # Get cardinality
                        cardinality = ""
                        if mod in ['*', '+', '?']:
                            cardinality = mod

                        # Create link
                        link = self._umlFrame.createNewLink(parent_oglClass, childOglClass, OGL_AGGREGATION)
                        pyutLink = link.getPyutObject()
                        pyutLink.setDestCard(cardinality)
                    elif len(tuple) == 3:
                        sep, cont, mod = tuple
                        # TODO : handle this
                    else:
                        raise Exception("Unsupported exception")

        # TODO : self._elementType.keys not in self._elementsTree.keys
        for parentElement in list(self._attribute.keys()):
            # test
            if parentElement not in elementsTree:
                displayError(_("Wrong DTD : An attribute refers to " + parentElement + ", but this is element is not declared."))
            else:
                # Get parent elements
                pyutClass = elementsTree[parentElement][0]

                # Read all attributes for the parent
                for attributesTuple in self._attribute[parentElement]:
                    attName, attType, attDecl, attDef = attributesTuple

                    # Create field
                    field = PyutField()
                    field.setName(attName)
                    field.setType(PyutType(str(attType) + " " + str(attDecl)))
                    if attDef != "None":
                        field.setDefaultValue(attDef)
                    pyutClass.addField(field)

    def new_general_entity(self, name, val):
        """
        Called when an internal general entity declaration is encountered.
        'val' contains the entity replacement text.
        """
        self._generalEntity[name] = val

    def new_external_entity(self, ent_name, pub_id, sys_id, ndata):
        """
        Called when an external general entity declaration is encountered.
        'ndata' is the name of the associated notation,
        or None if none was associated.
        """
        self._externalEntity[ent_name] = (pub_id, sys_id, ndata)

    def new_parameter_entity(self, name, val):
        """
        Called when an internal parameter entity declaration is encountered.
        'val' contains the entity replacement text.
        """
        self._parameterEntity[name] = val

    def new_external_pe(self, name, pubid, sysid):
        """
        Called when an external parameter entity declaration is encountered.
        """
        self._externalPe[name] = (pubid, sysid)

    def new_notation(self, name, pubid, sysid):
        """
        Called when a notation declaration is encountered.
        """
        self._notation[name] = (pubid, sysid)

    def new_element_type(self, elem_name, elem_cont):
        """
        Called when an element type declaration is encountered.
        'elem_cont' is a tuple, as returned by the get_content_model method
        of the ElementType interface.
        """
        self._elementType[elem_name] = elem_cont

    def new_attribute(self, elem, attr, a_type, a_decl, a_def):
        """
        Called when an attribute declaration is encountered.
        'elem' is the name of the element, 'attr' the name of the attribute,
        'a_type' the name of the attribute type (ID, CDATA...),
        'a_decl' the name of the declared default type (#REQUIRED, #IMPLIED...)
        and 'a_def' the declared default value (or None if none were declared).
        """
        if elem in self._attribute:
            self._attribute[elem].append((attr, a_type, a_decl, a_def))
        else:
            self._attribute[elem]=[(attr, a_type, a_decl, a_def)]

    def handle_comment(self, contents):
        """
        Called when a comment is encountered inside the DTD.
        """
        print(("Handle_comment ", contents))

    def handle_pi(self, target, data):
        """
        Called when a processing instruction is encountered inside the DTD.
        """
        print("handle_pi ", target, " /// ",  data)
