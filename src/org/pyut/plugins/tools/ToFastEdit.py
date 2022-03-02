
from typing import List
from typing import TextIO

from logging import Logger
from logging import getLogger

from os import system as osSystem
from os import remove as osRemove
from os import linesep as osLineSep

from sys import platform as sysPlatform
from typing import cast

from wx import CENTER
from wx import ICON_ERROR
from wx import ICON_EXCLAMATION
from wx import ID_OK
from wx import OK

from wx import MessageDialog

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutType import PyutType
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutParameter import PyutParameter
from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.ogl.OglClass import OglClass
from org.pyut.ogl.OglObject import OglObject
from org.pyut.plugins.base.PyutToPlugin import OglClasses

from org.pyut.ui.PyutProject import PyutProject
from org.pyut.ui.UmlFrame import UmlFrame

from org.pyut.plugins.base.PyutToPlugin import PyutToPlugin
from org.pyut.plugins.fastedit.DlgFastEditOptions import DlgFastEditOptions

from org.pyut.PyutConstants import PyutConstants

from org.pyut.general.Globals import _


class ToFastEdit(PyutToPlugin):

    FAST_EDIT_TEMP_FILE: str = 'pyut.fte'

    """
    """
    def __init__(self, umlObjects: OglClasses, umlFrame: UmlFrame):
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
        return "Fast Text Edit"

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
        return "Fast Text Edit"

    def setOptions(self) -> bool:
        """
        Returns:
            if `False` the action is cancelled.
        """
        ans: bool = True
        self.logger.debug(f"Before dialog show")

        with DlgFastEditOptions(self._umlFrame) as dlg:
            if dlg.ShowModal() == ID_OK:
                self.logger.info(f'Waiting for answer')
                self._editor = dlg.getEditor()
                if self._editor == "":
                    ans = False
            else:
                self.logger.info(f'Cancelled')

        self.logger.debug(f"After dialog show")
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

    def read(self, umlObject: OglClass, file: TextIO):
        """
        Read data from file

        format:
        ```python
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
        pyutClass: PyutClass = cast(PyutClass, umlObject.getPyutObject())
        pyutClass.name = className

        # process stereotype if present
        nextStereoType: str = file.readline().strip()
        if nextStereoType[0:2] == "<<":
            pyutClass.setStereotype(nextStereoType[2:-2].strip())
            nextStereoType = file.readline().strip()

        methods: List[PyutMethod] = []
        fields:  List[PyutField]  = []
        pyutClass.methods = methods
        pyutClass.fields  = fields

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
                vis = PyutVisibilityEnum.PUBLIC

            pos = nextStereoType.find("(")
            params = []
            if pos != -1:
                # process method
                name = nextStereoType[0:pos].strip()
                nextStereoType = nextStereoType[pos+1:]
                pos = nextStereoType.find(')')

                returnType: str = ""
                if pos != -1:
                    params = self._findParams(nextStereoType[:pos])
                    nextStereoType = nextStereoType[pos+1:]
                    pos = nextStereoType.find(":")

                    if pos != -1:
                        returnType = nextStereoType[pos+1:].strip()
                    else:
                        returnType = ""
                pyutType: PyutType   = PyutType(value=returnType)
                method:   PyutMethod = PyutMethod(name=name, visibility=vis, returnType=pyutType)

                method.setParams([PyutParameter(x[0], x[1]) for x in params])
                methods.append(method)
            else:
                # process field
                field = self._findParams(nextStereoType)[0]
                if field:
                    fields.append(PyutField(field[0], field[1], visibility=vis))

            nextStereoType = file.readline().strip()

    def write(self, oglObject: OglClass, file: TextIO):
        """
        Write data to filename.

        Format:
        ```python
        Class Name
        <<stereotype_optional>>
        +method([param[:type]]*)[:type_return]
        +field[:type][=value_initial]
        ```

        Args:
            oglObject:  The Ogl object to edit
            file:       The text file to write to
        """

        o: PyutClass = cast(PyutClass, oglObject.getPyutObject())

        file.write(o.getName() + osLineSep)

        if o.getStereotype() is not None:
            file.write(str(o.getStereotype()) + osLineSep)
        for method in o.methods:
            file.write(method.getString() + osLineSep)
        for field in o.fields:
            file.write(str(field) + osLineSep)

        file.close()

    def doAction(self, umlObjects: List[OglObject], selectedObjects: List[OglClass], umlFrame: UmlFrame):
        """

        Args:
            umlObjects: list of the uml objects of the diagram
            selectedObjects:  list of the selected objects
            umlFrame: the frame of the diagram
        """
        if len(selectedObjects) != 1:
            dlg: MessageDialog = MessageDialog(None, _("You must select at most a single class"), _("Warning"), OK | ICON_EXCLAMATION)
            dlg.ShowModal()
            dlg.Destroy()
            return
        oglClass: OglClass = selectedObjects[0]

        if isinstance(oglClass, OglClass) is False:
            dlg = MessageDialog(None, _('Must be a UML Class'), _('Bad Selection'), OK | ICON_ERROR | CENTER)
            dlg.ShowModal()
            dlg.Destroy()
            return

        filename: str = ToFastEdit.FAST_EDIT_TEMP_FILE

        self._writeTempTextFileForEditor(filename, oglClass)
        self._launchAppropriateEditor(filename)
        self._readTheModifiedTextFile(filename, oglClass)

        self._setProjectModified()
        self._cleanupTempFile()

    def _writeTempTextFileForEditor(self, filename: str, oglClass: OglClass) -> None:

        file: TextIO = open(filename, "w")
        self.write(oglClass, file)
        file.close()

    def _launchAppropriateEditor(self, filename: str) -> None:
        """
        Launches the configured editor in a platform appropriate way.  Assumes this blocks
        until the end-user exits the launched editor

        Args:
            filename: The file to pass to the editor
        """

        if sysPlatform == PyutConstants.THE_GREAT_MAC_PLATFORM:
            osSystem(f'open -W -a {self._editor} {filename}')
        else:
            osSystem(f'{self._editor} {filename}')

    def _readTheModifiedTextFile(self, filename: str, oglClass: OglClass):

        file: TextIO = open(filename, "r")
        self.read(oglClass, file)
        file.close()

    def _setProjectModified(self):

        fileHandling = self._ctrl.getFileHandling()
        project: PyutProject = fileHandling.getCurrentProject()
        if project is not None:
            project.setModified()

    def _cleanupTempFile(self):
        osRemove(ToFastEdit.FAST_EDIT_TEMP_FILE)
