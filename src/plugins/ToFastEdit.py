
from typing import List

from os import system

import UmlFrame

from plugins.PyutToPlugin import PyutToPlugin
from plugins.DlgFEOptions import DlgFEOptions

from OglObject import OglObject

from PyutMethod import PyutMethod
from PyutParam import PyutParam
from PyutField import PyutField


class ToFastEdit(PyutToPlugin):
    """
    Python code generation/reverse engineering

    @version $Revision: 1.5 $
    """
    def __init__(self, umlObjects: List[OglObject], umlFrame: UmlFrame):
        """
        Constructor.

        @param umlObjects : list of ogl objects
        @param umlFrame of pyut
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        PyutToPlugin.__init__(self, umlObjects, umlFrame)
        self._editor = None
        self._umlFrame = umlFrame

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        @since 1.1
        """
        return "Fast text edition"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        @since 1.1
        """
        return "Laurent Burgbacher <lb@alawa.ch>"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        @since 1.1
        """
        return "1.0"

    def getMenuTitle(self):
        """
        Return a menu title string

        @return string
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        # Return the menu title as it must be displayed
        return "Fast text edit"

    def setOptions(self):
        """
        Prepare the import.
        This can be used to ask some questions to the user.

        @return Boolean : if False, the import will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        dlg = DlgFEOptions(self._umlFrame)
        self._editor = dlg.getEditor()
        dlg.Destroy()

        if self._editor == "":
            return False

        return True

    def _findParams(self, line: str):
        """
        Parse a params line.

        format is :
        param:type[, param:type]*

        @param line
        @return []
        @since 1.0
        """
        # print "params received :", line
        params = [s.strip().split(":") for s in line.split(",")]
        params = [len(x) == 2 and x or [x[0], ""] for x in params]
        p = []
        # print "params:", params
        if params:
            for name, type in params:
                p.append((name.strip(), type.strip()))
        return p

    def read(self, umlObject, file):
        """
        Read data from filename. Abstract.

        format:
        Nom_de_la_classe
        <<stereotype_optionel>>
        +méthode([param[:type]]*)[:type_retour]
        +field[:type][=valeur_initiale]

        @param umlObject
        @param file
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        classname = file.readline().strip()
        pyutclass = umlObject.getPyutObject()
        pyutclass.setName(classname)

        # process stereotype if present
        nextStereoType = file.readline().strip()
        if nextStereoType[0:2] == "<<":
            pyutclass.setStereotype(nextStereoType[2:-2].strip())
            nextStereoType = file.readline().strip()

        methods = []
        fields = []
        pyutclass.setMethods(methods)
        pyutclass.setFields(fields)

        # process methods and fields
        while 1:
            if nextStereoType == "": break

            # search visibility
            if nextStereoType[0] in ("+", "-", "#"):
                vis = nextStereoType[0]
                nextStereoType = nextStereoType[1:]
            else:
                vis = ""

            pos = nextStereoType.find("(")
            params = []
            if pos != -1:
                # process method
                name = nextStereoType[0:pos].strip()
                nextStereoType = nextStereoType[pos+1:]
                pos = nextStereoType.find(")")
                if pos != -1:
                    params = self._findParams(nextStereoType[:pos])
                    nextStereoType = nextStereoType[pos+1:]
                    pos = nextStereoType.find(":")
                    if pos != -1:
                        returnType = nextStereoType[pos+1:].strip()
                    else:
                        returnType = ""
                method = PyutMethod(name, vis, returnType)
                method.setParams([PyutParam(x[0], x[1]) for x in params])
                methods.append(method)
            else:
                # process field
                field = self._findParams(nextStereoType)[0]
                if field:
                    fields.append(PyutField(field[0], field[1], visibility=vis))

            nextStereoType = file.readline().strip()

    def write(self, oglObject, file):
        """
        Write data to filename.

        format
        Nom_de_la_classe
        <<stereotype_optionel>>
        +méthode([param[:type]]*)[:type_retour]
        +field[:type][=valeur_initiale]

        @param oglObject
        @param file
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        import os
        o = oglObject.getPyutObject()
        file.write(o.getName() + "\n")
        if o.getStereotype() is not None:
            file.write(str(o.getStereotype()) + "\n")
        for method in o.getMethods():
            file.write(method.getString() + "\n")
        for field in o.getFields():
            file.write(str(field) + "\n")
        file.close()

    def doAction(self, umlObjects, selectedObjects, umlFrame):
        """
        Do the tool's action

        @param OglObject [] umlObjects : list of the uml objects of the diagram
        @param OglObject [] selectedObjects : list of the selected objects
        @param UmlFrame umlFrame : the frame of the diagram
        @since 1.0
        @author C.Dutoit <dutoitc@hotmail.com>
        """
        if len(selectedObjects) != 1:
            print("Please select one class")
            return
        filename = "pyut.fte"
        file = open(filename, "w")
        self.write(selectedObjects[0], file)
        system(self._editor + " " + filename)
        file = open(filename, "r")
        self.read(selectedObjects[0], file)
        file.close()
