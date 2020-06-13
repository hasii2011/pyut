from typing import List
from typing import Tuple
from typing import cast
from typing import Dict
from typing import NewType

from types import FunctionType

from logging import Logger
from logging import getLogger

from org.pyut.experimental.GraphicalHandler import GraphicalHandler

from org.pyut.model.PyutClass import PyutClass
from org.pyut.model.PyutField import PyutField
from org.pyut.model.PyutMethod import PyutMethod
from org.pyut.model.PyutParam import PyutParam
from org.pyut.model.PyutVisibilityEnum import PyutVisibilityEnum

from org.pyut.ogl.OglClass import OglClass

# from org.pyut.plugins.PluginAst import FieldExtractor
from org.pyut.plugins.FieldExtractor import FieldExtractor

from org.pyut.ui.UmlClassDiagramsFrame import UmlClassDiagramsFrame

ObjectMapType = NewType('ObjectMapType', Dict[str, OglClass])
KlassList     = NewType('KlassList', List[type])


class ReverseEngineerPython:

    def __init__(self):

        self.logger: Logger = getLogger(__name__)

    def reversePython(self, umlFrame: UmlClassDiagramsFrame, potentialTypes: List[type], files: Dict[type, str]):
        """
        Reverse engineering
        Classes come from introspection !!!

        Args:
            umlFrame:           The uml frame to display on
            potentialTypes:     The potential types from introspection
            files:   A map of introspected classes to the filename they came from
        """
        # get a list of classes info for classes in the display list
        klasses: KlassList = cast(KlassList, [cl for cl in potentialTypes if (type(cl) == type)])

        self.logger.info(f'classes: {klasses}')

        klasses = self._legacyLookup(klasses, potentialTypes)

        # create the PyutClass objects for each class
        objectMap: ObjectMapType = self._createPyutClassObjects(klasses, files, umlFrame)

        # now, search for parent links
        for oglClass in list(objectMap.values()):

            pyutClass: PyutClass = oglClass.getPyutObject()
            # skip object, it has no parent
            if pyutClass.getName() == "object":
                self.logger.info(f'pyutClass {pyutClass} has no parent')
                continue
            currentKlass: type = cast(type, None)
            for el in potentialTypes:
                if el.__name__ == pyutClass.getName():
                    currentKlass = el
                    break
            if currentKlass is None:
                self.logger.error("Reverse engineering error `currentKlass` is `None`")
                continue

            parentKlasses: List[type] = []
            try:
                parentKlasses = [cl for cl in klasses if cl.__name__ in [x.__name__ for x in currentKlass.__bases__]]
            except (ValueError, Exception) as e:
                self.logger.error(f'{e}')

            self._layoutInheritanceLinks(objectMap, oglClass, parentKlasses, umlFrame)

        objectList: List[OglClass] = list(objectMap.values())
        self._layoutUmlClasses(objectList, umlFrame)

    def _layoutInheritanceLinks(self, objectMap: ObjectMapType, oglClass: OglClass, parentKlasses: List[type], umlFrame: UmlClassDiagramsFrame):
        """

        Args:
            objectMap:
            oglClass:
            parentKlasses:
            umlFrame:

        """
        parentNames: List[str] = [item.__name__ for item in parentKlasses]
        for parent in parentNames:
            dest = objectMap.get(parent)
            if dest is not None:  # maybe we don't have the parent loaded
                graphicalHandler: GraphicalHandler = GraphicalHandler(umlFrame=umlFrame, maxWidth=umlFrame.maxWidth,
                                                                      historyManager=umlFrame.getHistory())
                graphicalHandler.createInheritanceLink(child=oglClass, parent=dest)

    def _layoutUmlClasses(self, objectList: List[OglClass], umlFrame: UmlClassDiagramsFrame):
        """
        Organize by vertical descending sizes

        Args:
            objectList:
            umlFrame:
        """
        # Sort by descending height
        sortedOglClasses = sorted(objectList, key=lambda oglClassToSort: oglClassToSort._height, reverse=True)
        x: int = 20
        y: int = 20

        incY: int = 0
        for oglClass in sortedOglClasses:
            incX, sy = oglClass.GetSize()
            incX += 20
            sy += 20
            incY = max(incY, sy)
            # find good coordinates
            if x + incX >= umlFrame.maxWidth:
                x = 20
                y += incY
                incY = sy
            oglClass.SetPosition(x, y)
            x += incX

    def _legacyLookup(self, klasses: KlassList, classesToReverseEngineer) -> KlassList:
        """
        Add extension class;
        TODO : I think this is old Python 2 code; put in warning to alert me if ever activated

        Args:
            klasses:  The current ones we know about
            classesToReverseEngineer:  The potential ones;  Maybe some are missing

        Returns
            Updated klass list
        """
        for cl in classesToReverseEngineer:
            try:
                if str(type(cl)).index("class") > 0:
                    if cl not in klasses:
                        self.logger.warning(f'Found a class with .`class` prefix `{cl}` not originally defined by `type`')
                        klasses.append(cl)
            except (ValueError, Exception) as e:
                self.logger.error(f'{e}')

        return klasses

    def _createPyutClassObjects(self, classes, files, umlFrame: UmlClassDiagramsFrame):

        objectMap: ObjectMapType = cast(ObjectMapType, {})  # Dictionary className/OglClass

        for cl in classes:
            try:
                # create objects
                pc: PyutClass = self.getPyutClass(cl, files[cl])
                po: OglClass = OglClass(pc)
                umlFrame.addShape(po, 0, 0)
                po.autoResize()
                objectMap[cl.__name__] = po
            except (ValueError, Exception) as e:
                self.logger.error(f"Error while creating class of type {cl},  {e}")

        return objectMap

    def getPyutClass(self, oglClass, filename: str = "", pyutClass=None):
        """
        If a pyutClass is input, it is modified in place.

        Args:
            oglClass:
            filename:   filename of the class
            pyutClass:  pyutClass to modify

        Returns:
            A PyutClass constructed from the Python class object OglClass.
        """
        import types
        from inspect import getfullargspec

        # Verify that parameters types are acceptable
        if type(oglClass) not in [type]:
            self.logger.error(f"IoPython/getPyutClass: Wrong parameter for oglClass:")
            self.logger.error(f"IoPython Expected class type, found {type(oglClass)}")
            return None

        # create objects
        cl = oglClass
        if pyutClass is None:
            pc: PyutClass = PyutClass(cl.__name__)       # A new PyutClass
        else:
            pc: PyutClass = pyutClass
        pc.setFilename(filename)          # store the class' filename
        methods: List[PyutMethod] = []    # List of methods for this class

        # Extract methods from the class
        klassMethods = [me for me in list(cl.__dict__.values()) if isinstance(me, types.FunctionType)]

        # Add the methods to the class
        for me in klassMethods:
            # Remove visibility characters
            if me.__name__[-2:] != "__":
                if me.__name__[0:2] == "__":
                    func_name = me.__name__[2:]
                elif me.__name__[0] == "_":
                    func_name = me.__name__[1:]
                else:
                    func_name = me.__name__
            else:
                func_name = me.__name__
            pyutMethod: PyutMethod = PyutMethod(func_name)     # A new PyutMethod

            # Add the method's params
            args = getfullargspec(me)
            if args[3] is None:
                firstDefVal = len(args[0])
            else:
                firstDefVal = len(args[0]) - len(args[3])
            for arg, i in zip(args[0], list(range(len(args[0])))):
                # don't add self, it's implied
                # defVal = None
                if arg != "self":
                    if i >= firstDefVal:
                        defVal = args[3][i - firstDefVal]
                        if type(defVal) == bytes:
                            defVal = '"' + defVal + '"'
                        param = PyutParam(arg, "", str(defVal))
                    else:
                        param = PyutParam(arg)
                    pyutMethod.addParam(param)

            self._addSourceCode(pyutMethod, me)
            methods.append(pyutMethod)

            # Set the visibility according to naming conventions
            if me.__name__[-2:] != "__":
                if me.__name__[0:2] == "__":
                    pyutMethod.setVisibility(PyutVisibilityEnum.PRIVATE)
                elif me.__name__[0] == "_":
                    pyutMethod.setVisibility(PyutVisibilityEnum.PROTECTED)
        # methods.sort(lambda x, y: cmp(x.getName(), y.getName()))
        sortedMethods = sorted(methods, key=lambda methodToSort: methodToSort._name)
        pc.methods = sortedMethods

        fields = None
        try:
            fe: FieldExtractor = FieldExtractor(pc.getFilename())
            fields: PyutField = fe.getFields(pc.getName())
            # fields = FieldExtractor(pc.getFilename()).getFields(pc.getName())
        except IOError:
            import sys
            import os
            self.logger.error(f"File {pc.getFilename()} not found in actual dir")
            self.logger.error(f"actual dir is {os.getcwd()}")
            for path in sys.path:
                try:

                    possibleFileName:    str = pc.getFilename()
                    possibleFQNFileName: str = f'{path}{os.sep}{possibleFileName}'
                    fe: FieldExtractor = FieldExtractor(possibleFQNFileName)
                    fields = fe.getFields(pc.getName())
                    break
                except IOError:
                    self.logger.error(f"Not found either in {path}{os.sep}{pc.getFilename()}")
                    pass
        if fields is None:
            self.logger.info(f"Could not extract from file {pc.getFilename()}")
        fds = []
        if fields:
            for name, init in fields.items():
                if init == "":
                    init = None
                vis: PyutVisibilityEnum = PyutVisibilityEnum.PUBLIC
                if len(name) > 1:
                    if name [-2:] != "__":
                        if name[0:2] == "__":
                            vis: PyutVisibilityEnum = PyutVisibilityEnum.PRIVATE
                            name = name[2:]
                        elif name[0] == "_":
                            vis: PyutVisibilityEnum = PyutVisibilityEnum.PROTECTED
                            name = name[1:]
                fds.append(PyutField(name, "", init, vis))

        # fds.sort(lambda x, y: cmp(x.getName(), y.getName()))
        sortedFields = sorted(fds, key=lambda fieldToSort: fieldToSort._name)
        pc.fields = sortedFields
        return pc

    def _addSourceCode(self, pyutMethod: PyutMethod, klassMethod: FunctionType):

        from inspect import getsourcelines

        methodName: str = pyutMethod.getName()
        source: Tuple[List[str], int] = getsourcelines(klassMethod)  # source list and line #

        sourceCode: PyutMethod.SourceCodeType = cast(PyutMethod.SourceCodeType, source[0])

        self.logger.info(f'Method: {methodName} - code: {sourceCode}')
        #
        # Source code always includes the method stanza
        #
        if len(sourceCode) > 1:
            firstLine: str = sourceCode.pop(0)
            self.logger.info(f'Removed: {firstLine}')

        pyutMethod.sourceCode = sourceCode
