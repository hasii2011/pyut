
from typing import List
from typing import TextIO

from logging import Logger
from logging import getLogger

from os import system as osSystem
from os import remove as osRemove

from sys import platform as sysPlatform

from wx import ICON_EXCLAMATION
from wx import ID_OK
from wx import MessageDialog
from wx import OK

from org.pyut.PyutConstants import PyutConstants
from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.ui.PyutProject import PyutProject
from org.pyut.ui.UmlFrame import UmlFrame

from org.pyut.plugins.PyutToPlugin import PyutToPlugin
from org.pyut.plugins.fastedit.DlgFastEditOptions import DlgFastEditOptions

from org.pyut.ogl.OglObject import OglObject

from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutField import PyutField

from org.pyut.general.Globals import _


class ToFastEdit(PyutToPlugin):

    FAST_EDIT_TEMP_FILE: str = 'pyut.fte'

    """
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

    def getName(self) -> str:
        """
        Returns:
            The name of the plugin.
        """
        return "Fast text edition"

    def getAuthor(self) -> str:
        """
        Returns:
            The author of the plugin.
        """
        return "Laurent Burgbacher <lb@alawa.ch>"

    def getVersion(self) -> str:
        """
        Returns:
            The version of the plugin.

        """
        return "1.0"

    def getMenuTitle(self) -> str:
        """
        Returns:
            A menu title string

        """
        # Return the menu title as it must be displayed
        return "Fast text edit"

    def setOptions(self) -> bool:
        """
        Returns:
            if `False` the import is cancelled.
        """
        ans: bool = True
        self.logger.info(f"Before dialog show")
        with DlgFastEditOptions(self._umlFrame) as dlg:
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
        Read data from file

        format:
        ```Python
        class name
        <<stereotype_optional>>
        +method([param[:type]]*)[:type_return]
        +field[:type][=value_initial]
        ```

        for example:

        ParentClass
        +strMethod(strParam : str = bogus) : str
        +intMethod(intParam = 1) : int
        +floatField : float = 1.0
        +booleanField : bool = True

        Args:
            umlObject:
            file:
        """
        className: str       = file.readline().strip()
        pyutClass: PyutClass = umlObject.getPyutObject()
        pyutClass.setName(className)

        # process stereotype if present
        nextStereoType: str = file.readline().strip()
        if nextStereoType[0:2] == "<<":
            pyutClass.setStereotype(nextStereoType[2:-2].strip())
            nextStereoType = file.readline().strip()

        methods = []
        fields = []
        pyutClass.setMethods(methods)
        pyutClass.setFields(fields)

        # process methods and fields
        visValues: List[str] = PyutVisibilityEnum.values()
        while True:
            if nextStereoType == "":
                break

            # search visibility

            if nextStereoType[0] in visValues:
                visStr = nextStereoType[0]
                vis: PyutVisibilityEnum = PyutVisibilityEnum.toEnum(visStr)
                nextStereoType = nextStereoType[1:]
            else:
                vis: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC

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
        Class Name
        <<stereotype_optional>>
        +method([param[:type]]*)[:type_return]
        +field[:type][=value_initial]

        @param oglObject
        @param file

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

    def doAction(self, umlObjects: List[OglObject], selectedObjects: List[OglObject], umlFrame: UmlFrame):
        """

        Args:
            umlObjects: list of the uml objects of the diagram
            selectedObjects:  list of the selected objects
            umlFrame: the frame of the diagram

        """
        if len(selectedObjects) != 1:
            dlg = MessageDialog(None, _("You must select at most a single class"), _("Warning"), OK | ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()

            return
        filename: str = ToFastEdit.FAST_EDIT_TEMP_FILE

        file: TextIO = open(filename, "w")
        self.write(selectedObjects[0], file)
        file.close()

        if sysPlatform == PyutConstants.THE_GREAT_MAC_PLATFORM:
            osSystem(f'open -W -a {self._editor} {filename}')
        else:
            osSystem(f'{self._editor} {filename}')
        file = open(filename, "r")
        self.read(selectedObjects[0], file)
        file.close()

        self._setProjectModified()
        self._cleanupTempFile()

    def _setProjectModified(self):

        fileHandling = self._ctrl.getFileHandling()
        project: PyutProject = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    def _cleanupTempFile(self):
        osRemove(ToFastEdit.FAST_EDIT_TEMP_FILE)
