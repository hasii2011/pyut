from typing import List
from typing import cast

import os

from pyutmodel.PyutLinkType import PyutLinkType
from pyutmodel.PyutClass import PyutClass
from pyutmodel.PyutField import PyutField
from pyutmodel.PyutMethod import PyutMethod

from org.pyut.plugins.base.PyutIoPlugin import PyutIoPlugin

from ogl import OglClass


class IoCpp(PyutIoPlugin):
    """
    C++ code generation

    @version $Revision: 1.2 $
    """
    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        return "C++ code generation"

    def getAuthor(self):
        """
        This method returns the plugin's author.

        Returns:  The author string

        """
        return "<droux@eivd.ch>"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        return "1.0"

    def getOutputFormat(self):
        """
        Return a specification tuple.

        @return tuple
        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        # return None if this plugin can't write.
        # otherwise, return a tuple with
        # - name of the output format
        # - extension of the output format
        # - textual description of the plugin output format
        # example : return ("Text", "txt", "Tabbed text...")
        return "C++ file", "cpp", "C++ file format"

    def setExportOptions(self) -> bool:
        return True

    def write(self, oglObjects):
        """
        Data Saving
        Args:
            oglObjects:  list of exported objects
        """

        print("Saving...")

        self._dir = self._askForDirectoryExport()
        try:
            os.mkdir(self._dir)
        except OSError:
            pass

        self._srcDir = self._dir + os.sep + "src"
        self._headerDir = self._dir + os.sep + "include"

        try:
            os.mkdir(self._srcDir)
        except OSError:
            pass

        try:
            os.mkdir(self._headerDir)
        except OSError:
            pass

        # defining constant
        self.__tab = "    "
        self.__demiTab = "  "
        self.__className = []

        for el in [oglObject for oglObject in oglObjects if isinstance(oglObject, OglClass)]:
            self._writeClass(cast(PyutClass, el.pyutObject))

        self.writeMain()
        self.writeMakefile()

        print("done !")

    def writeMain(self):

        main = open(self._srcDir + os.sep + 'main.cpp', 'w')

        for i in self.__className:
            main.write('#include "' + i + '.h"\n')

        main.write("""

int main(int argc, char** argv)
{
    ; //code here
}
        """)
        main.close()

    def _visibility(self, elements, public, private, protected):
        """
        TODO:  Fix this method so it returns a data structure that has this in/out lists

        Set all elements list in the lists to the appropriate visibility

        @param elements  : []  of object who has getVisibility methods.
        @param public    : []  list of public element
        @param private   : []  list of private element
        @param protected : []  list of protected element

        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        # for all element in list elements
        for element in elements:

            # getting element visibility
            visibility = str(element.visibility)

            # public case
            if visibility == '+':
                public.append(element)

            # private case
            elif visibility == '-':
                private.append(element)

            # protected case
            elif visibility == '#':
                protected.append(element)

    def _writeType(self, file, objType):
        """
        Writing objType in file.

        Default objType is void

        @param file
        @param objType      : String  represents a objType

        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        if objType == '':
            objType = "int"
        file.write(objType + " ")

    def _writeParam(self, file, param):
        """
        Writing param in file

        @param file
        @param param   : pyutParam

        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        # writing the objType
        self._writeType(file, str(param.type))
        # writing the param name
        file.write(param.name)

    def _writeMethod(self, file, method):
        """
        Writing a method in file : name(param, param, ...)

        @param file
        @param method    : pyutMethod

        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        # writing method name
        file.write(method.name + "(")
        # for all param
        nbParam = len(method.parameters)
        for param in method.parameters:
            # writing param
            self._writeParam(file, param)

            # default value
            if param.defaultValue is not None:
                file.write(" = " + param.defaultValue)

            # comma between param
            nbParam = nbParam - 1
            if nbParam > 0:
                file.write(" , ")
        file.write(")")

    def _fieldsWDefault(self, fields, defFields):
        for i in fields:
            if i.defaultValue is not None:
                defFields.append(i)

    def _writeSrcMethods(self, file, methods, className, fields):
        """
        Writing methods in source (.cpp) file

        @param file
        @param methods : [] list of all method of a class
        @param className : string the name of the class
        @param fields    : [] list of files whose are default value

        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        # for all method in methods list
        for method in methods:
            self._writeMethodComment(file, method, className)
            # writing objType
            # constructor case
            constructor = 1
            name = method.name
            if name != className and name != '~' + className:
                constructor = 0
                self._writeType(file, str(method.returnType))

            # writing class name
            file.write(className+"::")

            # writing method
            self._writeMethod(file, method)

            # if fathers --> initializing list
            if constructor:
                nbFields = len(fields)
                if nbFields > 0:
                    file.write(" : ")
                # for all fields who have a default value
                for field in fields:
                    if field.getDefaultValue() is not None:
                        file.write(field.name + '('+field.defaultValue + ')')
                        nbFields = nbFields - 1
                        if nbFields > 0:
                            file.write(" , ")

            file.write("\n{\n    ; // method code\n} // "+name+"\n\n")

    def _writeHeaderMethods(self, file, methods, className):
        """
        Writing methods in header (.h) file

        @param file
        @param methods : [] list of all method of a class
        @param className : string the name of the class

        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        # for all method in methods list
        for method in methods:

            self._writeMethodComment(file, method, className, self.__tab)
            # writing tab
            file.write(self.__tab)

            # writing objType
            # constructor case
            name = method.name
            if name != className and name != '~'+className:
                self._writeType(file, str(method.returnType))

            # writing method
            self._writeMethod(file, method)
            file.write(";\n\n")

    def _writeFields(self, file, fields):
        """
        Writing fields in file

        @param file
        @param fields : [] list of all fields of a class

        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        # for all field in fields list
        for field in fields:
            self._writeFieldComment(file, field.name, self.__tab)
            file.write(self.__tab)
            self._writeParam(file, field)
            file.write(";\n")

    def _writeLinks(self, file, links):
        """
        Writing link in file

        @param file
        @param links : [] list of all links

        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        # for all field in fields list
        for link in links:
            name = link.getDestination().name

            # for field name
            linkName = link.name
            if linkName == "":
                linkName = name[0].lower() + name[1:]

            self._writeFieldComment(file, linkName, self.__tab)
            file.write(self.__tab)
            file.write(name + ' ')

            # *
            if link.linkType == PyutLinkType.ASSOCIATION or link.linkType == PyutLinkType.AGGREGATION:
                file.write("*")

            file.write(linkName + ' ')
            file.write(";\n")

    # noinspection SpellCheckingInspection
    def _writeDefine(self, file, className):
        """
        Writing define instruction for pre-processor

        is writing in file :
        #ifndef __CLASSNAME_H__
        #define __CLASSNAME_H__

        Args:
            file:
            className: string the name of a class
        """
        define = "__"+className.upper()+"_H__"
        file.write("#ifndef "+define+"\n#define "+define+"\n\n\n")

    def _writeFathers(self, file, fathers):
        """
        Writing fathers for inheritance

        @param file
        @param fathers  : [] list of fathers

        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        nbr = len(fathers)

        # if is father for this class writing :
        if nbr > 0:
            file.write(" : ")

        for father in fathers:
            # writing fathers with public mode
            file.write("public " + father.name)

            # writing ',' between fathers
            nbr = nbr - 1
            if nbr > 0:
                file.write(", ")

    def _writeInclude(self, file, fathers, links):
        """
        Writing fathers for inheritance

        @param file
        @param fathers  : [] list of fathers
        @param links    : [] list of links

        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        # write name in include close
        # if the name is not in included dictionary
        def writeName():
            if name not in included:
                file.write('#include "' + name + '.h"\n')
                included[name] = 1

        # for all included file
        included = {}

        # include father
        for father in fathers:
            name = father.name
            writeName()

        # include link
        for link in links:
            name = link.getDestination().name
            writeName()

        file.write('\n')

    def _writeClassComment(self, file, className):
        """
        Writing class comment with doxygen organisation.

        @param file
        @param className    : String  represents a class

        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        file.write("/**\n * class "+className+"\n * More info here \n */\n")

    # noinspection PyUnusedLocal
    def _writeMethodComment(self, file, method, className, tab=""):
        """
        Writing method comment with doxygen organisation.

        @param file
        @param method    : pyutMethod

        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        # TODO use os.sep instead of hard code line feed
        file.write(tab + "/**\n")
        file.write(tab + " * method " + method.name+"\n")
        file.write(tab + " * More info here.\n")
        for param in method.parameters:
            file.write(tab + " * @param "+param.name + "   : ")
            self._writeType(file, str(param.type))
            file.write("\n")

        if str(method.returnType) != '':
            file.write(tab + " * @return " + str(method.returnType) + "\n")
        file.write(tab+" */\n")

    def _writeFieldComment(self, file, name, tab=""):
        """
        Writing method comment with doxygen organisation.

        @param file
        @param name    : field name

        @author D.Roux - droux@eivd.ch
        @since 1.1
        """
        file.write(tab + "/**\n")
        file.write(tab + " * field " + name+"\n")
        file.write(tab + " * More info here.\n")

        file.write(tab+" */\n")

    def _writeClass(self, pyutClass: PyutClass):
        """
        Writing a class to files

        Args:
            pyutClass:  an object pyutClass
        """

        className = pyutClass.name
        self.__className.append(className)

        # the two files and header (className.h) and
        #               a source (className.cpp) file
        headerFile = open(self._headerDir + os.sep+className + '.h',   'w')
        srcFile    = open(self._srcDir    + os.sep+className + '.cpp', 'w')

        # lists for files if there ar public, private or protected
        publicFields:    List[PyutField] = []
        privateFields:   List[PyutField] = []
        protectedFields: List[PyutField] = []
        defFields:       List[PyutField] = []

        fields: List[PyutField]  = pyutClass.fields
        self._visibility(fields, publicFields, privateFields, protectedFields)
        self._fieldsWDefault(fields, defFields)

        # lists for method if there ar public, private or protected
        publicMethods:    List[PyutMethod] = []
        privateMethods:   List[PyutMethod] = []
        protectedMethods: List[PyutMethod] = []
        self._visibility(pyutClass.methods, publicMethods, privateMethods, protectedMethods)

        fathers = pyutClass.getParents()
        links   = pyutClass.getLinks()

        # header define
        self._writeDefine(headerFile, className)

        # include file
        self._writeInclude(headerFile, fathers, links)
        srcFile.write('#include "' + className + '.h"\n\n')

        # class name
        self._writeClassComment(headerFile, className)
        self._writeClassComment(srcFile, className)
        headerFile.write("class " + className)

        self._writeFathers(headerFile, fathers)
        headerFile.write("\n{")

        # method and field

        # public part
        headerFile.write("\n"+self.__demiTab)
        headerFile.write("public :\n")
        srcFile.write("\n// public \n")
        self._writeSrcMethods(srcFile, publicMethods, className, defFields)
        self._writeHeaderMethods(headerFile, publicMethods, className)
        self._writeFields(headerFile, publicFields)

        # protected part
        headerFile.write("\n"+self.__demiTab)
        headerFile.write("protected :\n")
        srcFile.write("\n// protected \n")
        self._writeSrcMethods(srcFile, protectedMethods, className, defFields)
        self._writeHeaderMethods(headerFile, protectedMethods, className)
        self._writeFields(headerFile, protectedFields)

        # private part
        headerFile.write("\n"+self.__demiTab)
        headerFile.write("private :\n")
        srcFile.write("\n// private \n")
        self._writeLinks(headerFile, pyutClass.getLinks())
        self._writeSrcMethods(srcFile, privateMethods, className, defFields)
        self._writeHeaderMethods(headerFile, privateMethods, className)
        self._writeFields(headerFile, privateFields)

        # end of class
        headerFile.write("\n\n};\n#endif")

        headerFile.close()
        srcFile.close()

    def writeMakefile(self):
        makefile = open(self._dir + os.sep + 'Makefile', 'w')
        makefile.write("OBJS = ")

        for i in self.__className:
            makefile.write('src' + os.sep + i + ".o ")

        makefile.write(" src" + os.sep + "main.o")

        # TODO Leave tabs in this string;  Better yet externalize this as a file
        makefile.write("""

FILENAME = executable 
OPTIONS = -g -Wall -I./include
COMP = g++
LIBS = -lm

all: $(FILENAME)

%.o : %.cpp
	$(COMP) -c $(OPTIONS) $< -o src/$(@F)

$(FILENAME): $(OBJS)
	$(COMP) $(OPTIONS) $(OBJS) -o src/$(FILENAME) $(LIBS)
        """)

        makefile.close()
