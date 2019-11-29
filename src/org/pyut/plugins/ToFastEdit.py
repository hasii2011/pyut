
from logging import Logger
from logging import getLogger

from typing import List

from os import system

from wx import ID_OK

from org.pyut.ui.UmlFrame import UmlFrame

from org.pyut.plugins.PyutToPlugin import PyutToPlugin
from org.pyut.plugins.DlgFEOptions import DlgFEOptions

from org.pyut.ogl.OglObject import OglObject

from org.pyut.PyutMethod import PyutMethod
from org.pyut.PyutParam import PyutParam
from org.pyut.PyutField import PyutField


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
        super().__init__(umlObjects, umlFrame)

        self.logger: Logger = getLogger(__name__)
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

    def setOptions(self) -> bool:
        """

        @return Boolean : if False, the import will be cancelled.
        @author Laurent Burgbacher <lb@alawa.ch>
        @since 1.0
        """
        ans: bool = True
        self.logger.info(f"Before dialog show")
        with DlgFEOptions(self._umlFrame) as dlg:
            if dlg.ShowModal() == ID_OK:
                self.logger.info(f'Waiting for answer')
                self._editor = dlg.getEditor()
                if self._editor == "":
                    ans = False
            else:
                self.logger.info(f'Cancelled')

        self.logger.info(f"After dialog show")
        return ans

    def _findParams(self, line: str):
        """
        Parse a params line.

        format is :
        param:type[, param:type]*

        @param line
        @return []
        @since 1.0
        """
        self.logger.debug(f"params received: {line}")
        params = [s.strip().split(":") for s in line.split(",")]
        params = [len(x) == 2 and x or [x[0], ""] for x in params]
        p = []
        self.logger.debug(f"params: {params}")
        if params:
            for name, paramType in params:
                p.append((name.strip(), paramType.strip()))
        return p

    def read(self, umlObject, file):
        """
        Read data from filename

        format:
        class name
        <<stereotype_optionel>>
        +method([param[:type]]*)[:type_retour]
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
            if nextStereoType == "":
                break

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

                returnType: str = ""
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
            self.logger.info("Please select at least one class")
            return
        filename = "pyut.fte"
        file = open(filename, "w")
        self.write(selectedObjects[0], file)
        #
        # TODO:  Put a try catch block here;  This needs to work at least execute on a OS-X or Windoze
        #
        system(self._editor + " " + filename)
        file = open(filename, "r")
        self.read(selectedObjects[0], file)
        file.close()
