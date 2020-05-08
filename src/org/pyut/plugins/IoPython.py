
from typing import List
from typing import cast
from typing import Dict

from logging import Logger
from logging import getLogger

from os import sep as osSep
from os import path as osPath

from sys import path as sysPath

import importlib

from wx import CENTRE
from wx import ICON_INFORMATION
from wx import OK

from wx import BeginBusyCursor
from wx import EndBusyCursor
from wx import MessageBox
from wx import Yield as wxYield

from org.pyut.model.PyutClass import PyutClass
from org.pyut.ogl.OglClass import OglClass

from org.pyut.plugins.PyutIoPlugin import PyutIoPlugin
from org.pyut.plugins.base.PyutPlugin import PyutPlugin

from org.pyut.plugins.iopythonsupport.DlgAskWhichClassesToReverse import DlgAskWhichClassesToReverse
from org.pyut.plugins.iopythonsupport.PyutToPython import PyutToPython
from org.pyut.plugins.iopythonsupport.ReverseEngineerPython import ReverseEngineerPython

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

from org.pyut.general.Globals import _


class IoPython(PyutIoPlugin):

    """
    Python code generation/reverse engineering

    """
    def __init__(self, oglObjects, umlFrame):

        super().__init__(oglObjects=oglObjects, umlFrame=umlFrame)

        self.logger: Logger = getLogger(__name__)

        self._reverseEngineer: ReverseEngineerPython = ReverseEngineerPython()
        self._pyutToPython:    PyutToPython           = PyutToPython()

    def getName(self):
        """
        This method returns the name of the plugin.

        @return string
        """
        return "Python code generation/reverse engineering"

    def getAuthor(self):
        """
        This method returns the author of the plugin.

        @return string
        """
        return "C.Dutoit <dutoitc@hotmail.com> AND L.Burgbacher <lb@alawa.ch>"

    def getVersion(self):
        """
        This method returns the version of the plugin.

        @return string
        """
        return "1.0"

    def getInputFormat(self) -> PyutPlugin.INPUT_FORMAT_TYPE:
        """
        Return a specification tuple.
            name of the input format
            extension of the input format
            textual description of the plugin input format

        Returns:
            Return a specification tuple.
        """
        return cast(PyutPlugin.INPUT_FORMAT_TYPE, ("Python File(s)", "py", "Syntactically correct Python File"))

    def getOutputFormat(self) -> PyutPlugin.OUTPUT_FORMAT_TYPE:
        """
        Return a specification tuple.
            name of the output format
            extension of the output format
            textual description of the plugin output format

        Returns:
            Return a specification tuple.
        """
        return cast(PyutPlugin.OUTPUT_FORMAT_TYPE, ("Python File(s)", "py", "Syntactically correct Python File"))

    def setExportOptions(self) -> bool:
        return True

    def write(self, oglObjects: List[OglClass]):
        """

        Args:
            oglObjects:
        """
        directory = self._askForDirectoryExport()
        if directory == "":
            return False

        self.logger.info("IoPython Saving...")

        classes: Dict[str, List[str]] = {}
        generatedClassDoc: List[str] = self._pyutToPython.generateTopCode()

        # Create classes code for each object
        for oglClass in [oglObject for oglObject in oglObjects if isinstance(oglObject, OglClass)]:

            oglClass:  OglClass  = cast(OglClass, oglClass)
            pyutClass: PyutClass = oglClass.getPyutObject()

            generatedStanza:    str       = self._pyutToPython.generateClassStanza(pyutClass)
            generatedClassCode: List[str] = [generatedStanza]

            clsMethods: PyutToPython.MethodsCodeType = self._pyutToPython.generateMethodsCode(pyutClass)

            # Add __init__ Method
            if PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR in clsMethods:
                methodCode = clsMethods[PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR]
                generatedClassCode += methodCode
                del clsMethods[PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR]

            # Add others methods in order
            for pyutMethod in pyutClass.getMethods():
                methodName: str = pyutMethod.getName()
                if methodName != PyutToPython.SPECIAL_PYTHON_CONSTRUCTOR:
                    try:
                        methodCode: List[str] = clsMethods[methodName]
                        generatedClassCode += methodCode
                    except (ValueError, Exception, KeyError) as e:
                        self.logger.warning(f'{e}')

            generatedClassCode.append("\n\n")
            # Save to classes dictionary
            classes[pyutClass.getName()] = generatedClassCode

        # Write class code to a file
        for (className, classCode) in list(classes.items()):
            self._writeClassToFile(classCode, className, directory, generatedClassDoc)

        self.logger.info("IoPython done !")

        MessageBox(_("Done !"), _("Python code generation"), style=CENTRE | OK | ICON_INFORMATION)

    def _writeClassToFile(self, classCode, className, directory, generatedClassDoc):

        filename: str = f'{directory}{osSep}{str(className)}.py'

        file = open(filename, "w")
        file.writelines(generatedClassDoc)
        file.writelines(classCode)

        file.close()

    def read(self, oglObjects, umlFrame: UmlClassDiagramsFrame):
        """
        Reverse engineering

        Args:
            oglObjects:     list of imported objects
            umlFrame:       Pyut's UmlFrame
        """
        # Ask the user which destination file he wants
        # directory=self._askForDirectoryImport()
        # if directory=="":
        #    return False
        (lstFiles, directory) = self._askForFileImport(True)
        if len(lstFiles) == 0:
            return False

        # Add to sys.path
        sysPath.insert(0, f'{directory}{osSep}')

        self.logger.info(f'Directory added to sysPath = {directory}')
        umlFrame.setCodePath(directory)
        lstModules = []
        files = {}
        for filename in lstFiles:
            file = osPath.splitext(filename)[0]
            self.logger.info(f'Importing file={file}')

            try:
                module = __import__(file)
                importlib.reload(module)
                lstModules.append(module)
            except (ValueError, Exception) as e:
                self.logger.error(f"Error while trying to import file {file}, {e}")

        # Get classes
        classesDic = {}
        for module in lstModules:
            for cl in list(module.__dict__.values()):
                if type(cl) is type:
                    classesDic[cl] = 1
                    modname = cl.__module__.replace(".", osSep) + ".py"
                    files[cl] = modname
        classes = list(classesDic.keys())

        # Remove wx.Python classes ? TODO
        classes = self.askWhichClassesToReverse(classes)
        wxYield()
        if len(classes) == 0:
            return

        try:
            BeginBusyCursor()
            self._reverseEngineer.reversePython(umlFrame, classes, files)

        except (ValueError, Exception) as e:
            self.logger.error(f"Error while reversing engineering Python file(s)! {e}")
        EndBusyCursor()

    def getPyutClass(self, oglClass, filename: str = "", pyutClass=None):
        """
        TODO: BAD BAD BAD.  The ToPython plugin instantiates this plugin to get access to this method;
        Since I extracted the code I have to maintain this fiction;  This method probably belongs
        in a separate class;  However, I intend to separate the reverse engineer code from having
        to 'import' a class;  Importing means I have to satisfy class dependencies;  I
        will use the Python AST APIs to create the syntax trees I need for parsing

        If a pyutClass is input, it is modified in place.

        Args:
            oglClass:
            filename:   filename of the class
            pyutClass:  pyutClass to modify

        Returns:
            A PyutClass constructed from the Python class object OglClass.
        """
        return self._reverseEngineer.getPyutClass(oglClass=oglClass, filename=filename, pyutClass=pyutClass)

    def askWhichClassesToReverse(self, lstClasses):
        """
        Starts the dialog that asks which classes must be reversed

        Args:
            lstClasses: list of classes potentially reversible

        Returns:
            A list of classes to reverse-engineer
        """
        dlg = DlgAskWhichClassesToReverse(lstClasses)
        lstClassesChosen = dlg.getChosenClasses()
        dlg.Destroy()

        return lstClassesChosen
