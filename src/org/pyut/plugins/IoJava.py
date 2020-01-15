
from typing import cast

import os

from org.pyut.plugins.PyutIoPlugin import PyutIoPlugin

from org.pyut.ogl.OglClass import OglClass

from org.pyut.PyutLink import PyutLink

from org.pyut.enums.OglLinkType import OglLinkType


class IoJava(PyutIoPlugin):
    """
    Java code generation

    @version $Revision: 1.2 $
    """
    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        return "Java code generation"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        return "N. Dubois <nicdub@gmx.ch>"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        return "1.0"

    def getOutputFormat(self):
        """
        Return a specification tupple.

        @return tuple
        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        # return None if this plugin can't write.
        # otherwise, return a tupple with
        # - name of the output format
        # - extension of the output format
        # - textual description of the plugin output format
        # example : return ("Text", "txt", "Tabbed text...")
        return "Java", "java", "Java file format"

    def _writeParam(self, file, param):
        """
        Writing params in file.

        @param file
        @param param   : pyutParam

        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        # writing the param name
        file.write(str(param.getType()) + " " + param.getName())

    def _writeMethod(self, file, method):
        """
        Writing a method in file : name(param, param, ...).

        @param file
        @param method    : pyutMethod

        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        # Name of method
        name = method.getName()
        visibility = self.__visibility[str(method.getVisibility())]
        returnType = str(method.getReturns())
        if returnType == "":
            returnType = "void"

        # writing method name
        file.write(self.__tab + visibility + " " + returnType + " " + name + "(")
        # for all param
        nbParam = len(method.getParams())
        for param in method.getParams():
            # writing param
            self._writeParam(file, param)

            # comma between param
            nbParam = nbParam - 1
            if nbParam > 0:
                file.write(" , ")
        file.write(") {\n" + self.__tab + "}\n\n")

    # noinspection PyUnusedLocal
    def _writeMethods(self, file, methods, className):
        """
        Writing methods in source (.cpp) file

        @param file
        @param methods : [] list of all method of a class
        @param className : string the name of the class

        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        # Write header
        if len(methods) > 0:
            file.write("\n" + self.__tab + "// -------\n" + self.__tab + "// Methods\n" + self.__tab + "// -------\n\n")

        # for all method in methods list
        for method in methods:
            self._writeMethodComment(file, method, self.__tab)

            # writing method
            self._writeMethod(file, method)

    def _writeHeaderMethods(self, file, methods, className):
        """
        Writing methods in header (.h) file

        @param file
        @param methods : [] list of all method of a class
        @param className : string the name of the class

        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        # TODO
        # for all method in methods list
        for method in methods:

            # self._writeMethodComment(file, method, className, self.__tab)
            self._writeMethodComment(file=file, method=method, tab=self.__tab)
            # writing tab
            file.write(self.__tab)

            # writing type
            # constructor case
            name = method.getName()
            if name != className and name != '~'+className:
                self._writeType(file, str(method.getReturns()))

            # writing method
            self._writeMethod(file, method)
            file.write(";\n\n")

    def _writeFields(self, file, fields):
        """
        Write fields in file.

        @param file file:
        @param [PyutField, ...] fields : list of all fields of a class

        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        # Write fields header
        if len(fields) > 0:
            file.write(
                self.__tab + "// ------\n" + self.__tab + "// Fields\n" + self.__tab + "// ------\n\n")

        # Write all fields in file
        for field in fields:
            # Visibility converted from "+" to "public", ...
            visibility = self.__visibility[str(field.getVisibility())]

            # Type
            fieldType = str(field.getType())

            # Name
            name = field.getName()

            # Default value
            default = field.getDefaultValue()
            if default is not None and default != "":
                default = " = " + default
            else:
                default = ""

            # Comments
            if fieldType == "":
                comments = " // Warning: no type"
            else:
                comments = ""

            # Write the comment before the field
            self._writeFieldComment(file, name, self.__tab)

            # Write the complete line in file
            file.write(self.__tab + visibility + " " + fieldType + " " + name + default + ";" + comments + "\n")

    def _writeLinks(self, file, links):
        """
        Write relation links in file.

        @param file file:
        @param [] links : list of relation links
        """
        file.write("\n")
        # Write all relation links in file
        for link in links:
            link = cast(PyutLink, link)
            # Get Class linked (type of variable)
            destinationLinkName = link.getDestination().getName()
            # Get name of aggregation
            name = link.getName()
            # Array or single variable
            # if link.getDestinationCardinality().find('n') != -1:
            if link.destinationCardinality.find('n') != -1:
                array = "[]"
            else:
                array = ""

            # Write data in file
            file.write(self.__tab + "private " + destinationLinkName + " " + name + array + ";\n")

    def _writeFathers(self, file, fathers):
        """
        Writing fathers for inheritance.

        @param file file : class java file
        @param fathers  : [] list of fathers

        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        nbr = len(fathers)

        # If there is a father:
        if nbr != 0:
            file.write(" extends ")

            # Only one father allowed
            file.write(fathers[0].getName())

    def _writeInterfaces(self, file, interfaces):
        """
        Writing interfaces implemented by the class.

        @param file file : class java file
        @param interfaces  : [] list of fathers

        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        nbr = len(interfaces)

        # If there is at least one interface:
        if nbr != 0:
            file.write(" implements ")

            # Write the first interface
            file.write(interfaces[0].getDestination().getName())

            # For all next interfaces, write the name separated by a ','
            for interface in interfaces[1:]:
                file.write(", " + interface.getDestination().getName())

    def _writeClassComment(self, file, className, classInterface):
        """
        Write class comment with doxygen organisation.

        @param file
        @param className    : String  represtent a class

        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        file.write("/**\n * " + classInterface + " " + className + "\n * More info here \n */\n")

    def _writeMethodComment(self, file, method, tab=""):
        """
        Write method comment with doxygen organisation.

        @param file file : java file
        @param method    : pyutMethod

        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        file.write(tab + "/**\n")
        file.write(tab + " * method " + method.getName()+"\n")
        file.write(tab + " * More info here.\n")
        for param in method.getParams():
            file.write(tab + " * @param " + param.getName() + " : " + str(param.getType()) + "\n")

        if str(method.getReturns()) != '':
            file.write(tab + " * @return " + str(method.getReturns()) + "\n")
        file.write(tab + " */\n")

    def _writeFieldComment(self, file, name, tab=""):
        """
        Write method comment with doxygen organisation.

        @param file
        @param name    : field name

        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1
        """
        file.write(tab + "/**\n")
        file.write(tab + " * field " + name+"\n")
        file.write(tab + " * More info here.\n")

        file.write(tab+" */\n")

    def _seperateLinks(self, allLinks, interfaces, links):
        """
        Seperate the differents types of links into lists.

        @param [PyutLinks] links : list of links of the class
        @param [str] interfaces : list of interfaces implemented by the class

        @author N. Dubois <nicdub@gmx.ch>
        @since 1.1.2.2
        """
        for link in allLinks:
            linkType = link.getType()
            if linkType == OglLinkType.OGL_INTERFACE:
                interfaces.append(link)
            elif linkType == OglLinkType.OGL_COMPOSITION or linkType == OglLinkType.OGL_AGGREGATION:
                links.append(link)

    def _writeClass(self, pyutClass):
        """
        Writing a class to files.

        @param pyutClass : an object pyutClass
        """
        # Read class name
        className = pyutClass.getName()

        # Opening a file for each class
        javaFile = open(self._dir+os.sep+className+'.java', 'w')

        # Extract the datas from the class
        fields     = pyutClass.getFields()
        methods    = pyutClass.getMethods()
        fathers    = pyutClass.getParents()
        allLinks   = pyutClass.getLinks()
        stereotype = pyutClass.getStereotype()

        # List of links
        interfaces = []     # List of interfaces implemented by the class
        links      = []     # Aggregation and compositions
        self._seperateLinks(allLinks, interfaces, links)

        # Is this class an interface
        # ~ self._isInterface(pyutClass)

        # Is it an interface
        classInterface = "class"
        if stereotype is not None:
            stereotype = stereotype.getStereotype()
            if stereotype == "Interface":
                classInterface = "interface"

        # Write data in file
        # -------------------

        # Write class comment
        self._writeClassComment(javaFile, className, classInterface)
        # class name
        javaFile.write("public " + classInterface + " " + className)

        self._writeFathers(javaFile, fathers)
        self._writeInterfaces(javaFile, interfaces)
        javaFile.write(" {\n\n")

        # Fields
        self._writeFields(javaFile, fields)

        # Aggregation and Composition
        self._writeLinks(javaFile, links)
        # Methods
        self._writeMethods(javaFile, methods, className)
        # end of class
        javaFile.write("}\n")

    def write(self, oglObjects):
        """
        Data saving
        @param oglObjects : list of exported objects
        """
        # Directory for sources
        self._dir = self._askForDirectoryExport()

        # If no destination, abort
        if self._dir == "":
            return

        # defining constant
        self.__tab = "    "
        self.__visibility = {
            "+": "public",
            "-": "private",
            "#": "protected"
        }

        for el in [object for object in oglObjects if isinstance(object, OglClass)]:
            self._writeClass(el.getPyutObject())
